import torch
from enum import Enum
from src.utils import get_size_from_chars, GPT2_BLOCK_SIZE
from src.torch_loader.vectorize_input import TrainInput, GenerationInput


class VectorizeMode(Enum):
    """
    Defines the 3 possible modes of our model: Training, Evaluation, Generation
    """
    TRAIN = 0
    EVAL = 1
    GENERATE = 2


class VectorizeParagraph:
    """
    class VectorizeParagrah
    An instance of this class will be callable on {input: (metadata, P1, P3), target: P2}
    """

    def __init__(self,
                 tokenizer,
                 block_size=GPT2_BLOCK_SIZE,
                 mode=VectorizeMode.TRAIN):
        """
        Store the parameters of the vectorizer, by default : mode = Train, use_context = True
        :param block_size : int, max sequence_token_len for GPT_2 input
        :param mode: VectorizerMode

        """
        self.tokenizer = tokenizer
        self.block_size = block_size
        self.mode = mode
        

    @staticmethod
    def concat_context(context_d):
        """
        Concatanate the context_dict in the order
            [COALICION]  [PARTIDO] [SENTIMIENTO] [ENTIDADES] [HASHTAGS] [FRASES]  [TWEET] 
        :param context_d: [dict] containing the context
        :return: concatanate of context_d values in the right order
        """
        return context_d['COALICION'] + context_d['PARTIDO'] + context_d['SENTIMIENTO'] + context_d['ENTIDADES'] + context_d['HASHTAGS']+ context_d['FRASES'] + context_d['TWEET']

    def vectorize(self, context, TWEET, nb_tokens_for_TWEET):
        
        
        """
        :param context: [dict] representing the context
        :param TWEET: [str] True TWEET or '' in generation_mode
        :param nb_tokens_for_TWEET: nb of tokens in true TWEET or nb of tokens to saved for P2 in generation mode
        :return: vectorize version of the dict
        """
        

        nb_tokens_for_context = sum(map(len, context.values()))  # Context = everything except P2

        if self.mode == VectorizeMode.TRAIN:
            # In train mode, TWEET is added to the context and the sentence to predict is simplify the full context
            context['TWEET'] += self.tokenizer.encode(TWEET + ' ' + '<|endoftext|>') 
            
        old_len = nb_tokens_for_context + nb_tokens_for_TWEET
        
        if (old_len >= self.block_size):
            needed = old_len - self.block_size +7
            
            
            nkp = len(context['FRASES'])
            nen = len(context['ENTIDADES'])
            ntw = len(context['TWEET'])
            
            if needed <= nkp:
                tokens_para_frases = nkp - needed 
                context['FRASES'] = context['FRASES'][:tokens_para_frases]
                needed = needed - nkp
            else:
                needed = needed - nkp
                context['FRASES'] = []
                
            if needed > 0:
                
                if needed <= nen:
                    tokens_para_entidades = nen - needed
                    context['ENTIDADES'] = context['ENTIDADES'][:tokens_para_entidades]
                    needed = needed - nen
                else:
                    needed = needed - nen
                    context['ENTIDADES'] = []
                  
            if needed > 0:
                tokens_para_tweets = ntw - needed
                context['TWEET'] = context['TWEET'][:tokens_para_tweets]
                needed = needed - ntw
                
                
        new_len  = sum(map(len, context.values()))
        
        #if old_len >= self.block_size:
        #    print('len: {}->{}'.format(old_len, new_len))
            
      

        token_types = {key: [value[0]] * len(value) if len(value) > 0 else [] for key, value in context.items()}
              
        tensor_input = torch.tensor(self.concat_context(context))
        tensor_types = torch.tensor(self.concat_context(token_types))
        
        assert len(tensor_input) == len(tensor_types)

        if self.mode == VectorizeMode.TRAIN:
            labels = torch.tensor(
                [-100] * (sum(len(v) for k, v in context.items() if k != 'TWEET') + 1) + context['TWEET'][1:])
    
            
            assert len(labels) == len(tensor_input)
            return tensor_input, tensor_types, labels
        else:
            return tensor_input, tensor_types

    def __call__(self, sample):
        """
        Create an input_dict which formats and encodes (using GPT2 tokenizer) the data

        :param sample: [TrainInput] object in train and evaluation mode
                       [GenerationInput] ojbect in generation mode

        :return:
            for train mode:
                with context : [P3] P3 [Sum] Sum_P2 [T] Theme [Ent] list_of_person [Size] [P1] P1 [P2] P2 <|endoftext|>
                without context : P1 P2

            for eval mode:
                with context : [P3] P3 [Sum] Sum_P2 [T] Theme [Ent] list_of_person [Size] [P1] P1 [P2], sample
                witouht context : P1, sample

            for generate mode:
                with context: [P3] P3 [Sum] Sum_P2 [T] Theme [Ent] list_of_person [Size] [P1] P1 [P2]
                witout context : P1
        """
        if self.mode == VectorizeMode.TRAIN or self.mode == VectorizeMode.EVAL:
            assert type(sample) == TrainInput, 'In train/eval mode, vectorizer input must be of type TrainInput'

        if self.mode == VectorizeMode.GENERATE:
            assert type(
                sample) == GenerationInput, 'In generation mode, vectorizer input must be of type GenerationInput'

        context = dict()
        context['COALICION'] = ' [COALICION] ' + sample.COALICION if sample.COALICION != "" else ""
        context['PARTIDO'] = ' [PARTIDO] ' + sample.PARTIDO if sample.PARTIDO != "" else ""
        context['SENTIMIENTO'] = ' [SENTIMIENTO] ' + sample.SENTIMIENTO if sample.SENTIMIENTO != "" else ""
        context['ENTIDADES'] = ' [ENTIDADES] ' + sample.ENTIDADES if sample.ENTIDADES != "" else ""
        context['HASHTAGS'] = ' [HASHTAGS] ' + sample.HASHTAGS if sample.HASHTAGS != "" else ""
        context['FRASES'] = ' [FRASES] ' + sample.FRASES if sample.FRASES != "" else ""
        context['PARTIDO'] = ' [PARTIDO] ' + sample.PARTIDO if sample.PARTIDO != "" else ""
        context['TWEET'] = ' [TWEET] ' 


        # Encode the context

        for key, value in context.items():
            context[key] = self.tokenizer.encode(value)

        # In generate mode, obviously, the true P2 doest not exist
        TWEET = sample.TWEET if self.mode != VectorizeMode.GENERATE else ""

        # Compute the number of tokens we saved for TWEET in the input block
        if self.mode == VectorizeMode.GENERATE:
            nb_tokens_for_TWEET = 200 + 50
        else:
            nb_tokens_for_TWEET = len(self.tokenizer.encode(TWEET)) + 2  # +1 for [TWEET] and +1 for <|endoftext|>

        if self.mode == VectorizeMode.TRAIN:
            input_ids, type_ids, labels = self.vectorize(context, TWEET, nb_tokens_for_TWEET)
            return input_ids, type_ids, labels

        if self.mode == VectorizeMode.GENERATE:
            input_ids, type_ids = self.vectorize(context, TWEET, nb_tokens_for_TWEET)
            return input_ids, type_ids

        if self.mode == VectorizeMode.EVAL:
            input_ids, type_ids = self.vectorize(context, TWEET, nb_tokens_for_TWEET)
            return input_ids, sample, nb_tokens_for_TWEET
