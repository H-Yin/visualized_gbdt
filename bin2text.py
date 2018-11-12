import xgboost as xgb
import getopt as opt


MODEL_PATH = ''
FEATURE_PATH = ''
TYPE = None
OUTPUT_PATH = ''

def usage():
    help_text= '''
Usage: dumpBin [OPTION] args 
       dumpBin help
options:
    -m, --model MODEL_PATH     model's dump file, specified.
    -f, --feature FEATURE_PATH feature's file, specified.
    -o, --output OUTPUT_PATH   output path.
    -t, --type type             the format of output file.
    '''
    print help_text

def getOpts(argv):
    global FEATURE_PATH, MODEL_PATH, BOOSTER_NUM, DEPTH, OUTPUT_PATH
    try:
        options, args = opt.getopt(argv[1:], '-m:-f:-t:-o:-h', ['feature=','model=', 'type=','output=','help'])
        for op, value in options:
            if op in ('-h','--help'):
                usage()
                sys.exit()
            if op in ('-f', '--feature'):
                FEATURE_PATH = value
            if op in ('-m', '--model'):
                MODEL_PATH = value
            if op in ('-t', '--type'):
                TYPE = value
            if op in ('-o', '--output'):
                OUTPUT_PATH = value
        if FEATURE_PATH == '' or MODEL_PATH == '':
            usage()
            sys.exit()
    except opt.GetoptError:
        usage()
        sys.exit()

def dumpBin(model_path, feature_map='', out_put='' ,ftype=''):
    bst = xgb.load_model(mode_path)
    bst.dump_model(out_put, fmap=freature_map, with_stats=True, dump_format=ftype)


if __name__ == '__main__':
    # get options
    getOpts(sys.argv)
    dumpBin(MODEL_PATH, FEATURE_PATH, OUTPUT_PATH, TYPE)
