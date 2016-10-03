import sklearn
import inspect


default_learner = "RandomForestRegressor"
try:
    import xgboost as xgb
    default_learner = "XGBRegressor"
except: pass

try: import autosklearn.classification
except: pass

try: import evolutionary_search
except: pass

try: import TimeSeriesEstimator
except: pass

try: from TimeSeriesEstimator import TimeSeriesRegressor
except: pass


#try: import mlp
#except: pass

    
class Autostat_SKLearn(Autostat):
    def __init__(self, o=None):
        
        if o: 
            
            super(Autostat_SKLearn, self).__init__(o=o)
        else: 
            
            super(Autostat_SKLearn, self).__init__()
        

    def custom_init(self):
        
        import warnings
        warnings.filterwarnings("ignore")
        self.skengines = {}
        packages = []
        for package in sklearn.__all__:
            packages.append(["sklearn", package])
            
        classes_to_test = []

        for i in packages:
            try: 
                __import__(".".join(i))
                classes_to_test.append(getattr(sklearn, i[1]))
            except: pass

        for thing in dir(xgb):
            try: classes_to_test.append(getattr(xgb, thing))
            except: pass
        
        try: classes_to_test.append(autosklearn.classification)
        except: pass
        
        try: classes_to_test.append(evolutionary_search)
        except: pass

        try: classes_to_test.append(mlp)
        except: pass

        try: classes_to_test.append(TimeSeriesEstimator)
        except: pass

        for class_to_test in classes_to_test:
            for learner in dir(class_to_test):
                try:
                    l = getattr(class_to_test, learner)
                    if hasattr(l, 'predict') and hasattr(l, 'fit'):
                        self.skengines[l.__name__]=l
                except:pass


    def collect_options(self):
        
        super(Autostat_SKLearn, self).collect_options()
        group = optparse.OptionGroup(self.parser, "SKLearn Options")
        group.add_option("", "--sk-engine", dest="skenginename", default=default_learner, help="Specify scikit-learn engine.  Use 'help' to list all candidates")
        group.add_option("", "--sk-help", dest="skhelp", default=False, action="store_true", help="Print help for scikit-learn engine.")
        group.add_option("", "--sk-get-params", dest="skgetparams", default="", action="store_true", help="Print params for scikit-learn engine.")
        group.add_option("", "--sk-set-params=", dest="sksetparams", default=False, help="Set params for scikit-learn engine.")
        #group.add_option("", "--sk-tsr", dest="sktsr", default=False, action="store_true", help="Create Time Series Regression")
        #group.add_option("", "--sk-tsr-prev", dest="sktsr_prev", default=3, type=int, help="Use this many samples (default 3) to predict future")
        #group.add_option("", "--sk-tsr-next", dest="sktsr_next", default=20, type=int, help="Predict this number of outputs (default 20)")
        self.parser.add_option_group(group)

    def add_options(self):
        
        super(Autostat_SKLearn, self).add_options()
        if self.o.skenginename == "help":
            for learner in self.skengines.keys():
                print learner
            sys.exit(1)
        if self.o.skhelp:
            help(self.skengines[self.o.skenginename])
            sys.exit(2)
        self.skengine = None
        if self.o.sksetparams:
            params = {}
            try:
                params = json.loads(self.o.sksetparams)
            except:
                paramlist = self.o.sksetparams.split(",")
                for paramset in paramlist:
                    k,v = paramset.split("=")
                    if v.isdigit(): v = int(v)
                    params[k]=v
            self.skengine = self.skengines[self.o.skenginename](**params)
        if not self.skengine: self.skengine=self.skengines[self.o.skenginename]()
        if self.o.skenginename.find("XGB")==0:
            if self.o.rounds==0: self.o.rounds=200
            self.skengine.set_params(n_estimators=self.o.rounds)
        if self.o.skgetparams:
            print >> sys.stderr, "ENGINE: ", self.o.skenginename
            s = []
            params = self.skengine.get_params()
            for k in params.keys():
                v = str(params[k])
                s.append("=".join([k,v]))
            print ',\n'.join(s)
            #print >> sys.stderr, self.skengine.get_params()
            sys.exit(3)

    def train(self):
        
        size=len(self.df)
        
        if self.o.skenginename.find("XGB")==0:
        
            self.df = self.df[0:int(size*0.8)]
            self.testdf = self.df[:int(size*0.2)]
            
        opts = {}
        opts["y"] = np.array(self.df[self.o.target])
        opts["X"] = np.array(self.df.drop(self.o.target,axis=1))
        tX=ty=None
        if self.o.skenginename.find("XGB")==0:
            ty = np.array(self.testdf[self.o.target])
            tX = np.array(self.testdf.drop(self.o.target,axis=1))
            opts["eval_set"] = [(opts["X"], opts["y"]), (tX, ty)]
            opts["eval_metric"] = "logloss"
            opts["verbose"] = not self.o.quiet
            opts["early_stopping_rounds"]=100
            #self.skengine.set_params(n_estimators=100000)
        self.model = self.skengine.fit(**opts)
        


register_engine(Autostat_SKLearn, canHandle={"classification": True, "regression": True})
