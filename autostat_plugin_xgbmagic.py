import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

import xgbmagic

class Autostat_XGBMagic(Autostat):
    def __init__(self, o=None):
        if o: super(Autostat_XGBMagic, self).__init__(o=o)
        else: super(Autostat_XGBMagic, self).__init__()

    def set_model(self):
        super(Autostat_XGBMagic, self).set_model()
        target_type=None
        if self.o.mode == "classification":
            target_type = "multiclass"
            if len(self.df[self.o.target].unique())==2:
                target_type="binary"
                self.df[self.o.target]=self.df[self.o.target].astype(bool)
            else:
                self.df[self.o.target]=self.df[self.o.target].astype(int)
        else:
            target_type = "linear"
        cat_columns = []
        for colname in self.df.columns:
            if self.featuremap[colname]["colType"]=="categorical" and colname!=self.o.target:
                cat_columns.append(colname)
        self.model = xgbmagic.Xgb(self.df, target_column=self.o.target, target_type=target_type,
                           categorical_columns=cat_columns,
                           num_training_rounds=2000, early_stopping_rounds=50, verbose=True)

    def train(self):
        # no superclass call
        self.model.train()
        
    def predict(self):
        # no superclass call
        self.predictions = self.model.predict(self.df)
    
    def report(self):
        super(Autostat_XGBMagic, self).report()
        print self.model.feature_importance()
        


register_engine(Autostat_XGBMagic)
