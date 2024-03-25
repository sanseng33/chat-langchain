from prettytable import PrettyTable
import time
import openai
from openai import OpenAI
from tqdm import tqdm
import itertools
import wandb
from tenacity import retry, stop_after_attempt, wait_exponential

use_wandb = False # set to True if you want to use wandb to log your config and results

use_portkey = False

client = OpenAI()