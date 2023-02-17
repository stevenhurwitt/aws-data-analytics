import datetime as dt
import pandas as pd
import numpy as np
from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.column import *
from pyspark.sql.types import *
import pprint
import yaml
import json
import time
import sys
import os

pp = pprint.PrettyPrinter(indent = 1)

def main():

    print("hello world.")
    with open("creds.json", "r") as f:
        creds = json.load(f)
        f.close()

    pp.pprint(creds)

if __name__ == "__main__":
    main()
