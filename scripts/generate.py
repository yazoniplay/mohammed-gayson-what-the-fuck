from pathlib import Path
import argparse
from generate_script import generate
def main():
 p=argparse.ArgumentParser(); p.add_argument("--topic",required=True); p.add_argument("--profile",default="youtube",choices=["youtube","shorts","square","4k"]); a=p.parse_args()
 run=Path("data/runs")/a.topic.lower().replace(" ","-")[:50]; run.mkdir(parents=True,exist_ok=True)
 print("script:",generate(a.topic,run/"script.json")); print("profile:",a.profile); print("Next: narration -> alignment -> assets -> manifest -> Remotion.")
if __name__=="__main__": main()
