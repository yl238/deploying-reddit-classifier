import re
import spacy
import unicodedata
import inflect
import contractions
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils import resample


nlp = spacy.load('en_core_web_sm')

class InputTextCreator(BaseEstimator, TransformerMixin):
    def __init__(self, features=None, text_field=None):
        self.output = text_field
        if features is not None:
            if not isinstance(features, list):
                self.features = [features]
            else:
                self.features = features

    def fit(self, X, y=None):
        return self
    
    def _concatenate(self, X):
        X[self.output] = X[self.features].fillna('').agg(' '.join, axis=1)
        return X
    
    def transform(self, X):
        return self._concatenate(X)


class MajorityClassDownsampler(BaseEstimator, TransformerMixin):
    def __init__(self, target=None, majority_class=None, sample_fraction=1, random_state=42):
        self.target = target
        self.class_name = majority_class
        self.sample_fraction = sample_fraction
        self.random_state = random_state
    
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        df_majority = X[X[self.target] == self.class_name]
        df_others = X[X[self.target] != self.class_name]
        
        n_samples = int(len(df_majority) * self.sample_fraction)
    
        majority_downsampled = resample(df_majority, replace=False, 
                                        n_samples=n_samples, 
                                        random_state=self.random_state)
        downsampled = pd.concat([majority_downsampled, df_others])
        return downsampled


class TextCleaner(BaseEstimator, TransformerMixin):
    def __init__(self, variable=None):
        self.variable = variable
            
    def _remove_https_links(self, text):
        return re.sub(r'https?://\S+', '', text, flags=re.MULTILINE)

    def _replace_non_alphanumeric(self, text):
        return re.sub(r'[^\w\'\$ ]', ' ', text, flags=re.MULTILINE)

    def _denoise_text(self, text):
        text = self._remove_https_links(text)
        text = self._replace_non_alphanumeric(text)
        return text

    def _replace_contractions(self, text):
        return contractions.fix(text)

    def _normalize(self, text):
        text = self._denoise_text(text)
        text = self._replace_contractions(text)
        return text.lower()
                    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        X[self.variable] = X[self.variable].apply(self._normalize)
        return X


class TextTokenizer(BaseEstimator, TransformerMixin):
    def __init__(self, variable=None, stopword_exceptions=None):
        self.variable = variable
        if stopword_exceptions:
            nlp.Defaults.stop_words -= set(list(stopword_exceptions))
            
    def _lemmatize_and_remove_stop_words(self, text):
        return [t.lemma_ for t in nlp(text) if not t.is_stop and len(t.lemma_) > 1]
    
    def _normalize(self, text):
        words = self._lemmatize_and_remove_stop_words(text)
        return ' '.join(words)
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        X[self.variable] = X[self.variable].apply(self._normalize)
        return X[self.variable]
