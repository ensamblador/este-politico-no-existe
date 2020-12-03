from torch.utils.data import Dataset
from src.torch_loader.vectorize_input import TrainInput
import json
import pandas as pd


class DatasetFromPandas(Dataset):
    """
    DatasetFromFile :
    generate vectorize samples (coalicion, partido, entidades... ; tweet) from a dataframe

    main idea :
        1/ will generate (nb_paragraphes - 2) tupple (input, label)
        2/ will apply a GPT_2 tokenization for each input, label
    """

    def __init__(self, df, transform):
        """
        :param df: Pandas Dataframe
        :param transform: transform: function to transform paragraph into a vectorized form (GPT_2 tokenization
        """
        self.data = df
        self.transform = transform
        self.length = len(df) 

    def __len__(self):
        """
        :return: number of paragraphes in the novel 
        """
        return self.length

    def __getitem__(self, idx):
        """
        :return: vectorized (COALICION, PARTIDO, SENTIMIENTO, ENTIDADES, HASHTAGS, FRASES, TWEET)
        """
        COALICION, PARTIDO, SENTIMIENTO, ENTIDADES, HASHTAGS, FRASES, TWEET = self.data.iloc[idx]


        training_example = TrainInput(
            COALICION=COALICION,
            PARTIDO=PARTIDO,
            SENTIMIENTO=SENTIMIENTO,
            ENTIDADES=ENTIDADES,
            HASHTAGS=HASHTAGS,
            FRASES=FRASES,
            TWEET=TWEET
        )
    
        return self.transform(training_example)
