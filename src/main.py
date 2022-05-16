import fontprocessing
import endprocessing
import os
import os.path
import argparse

if __name__ == "__main__":
    # TODO: phase args
    parser = argparse.ArgumentParser(description="Kison's mcu font tool")
    parser.add_argument("-c","--config",help="Path of config yaml, default config if not provided",required=False) 
    parser.add_argument("-t", "--target", help="Path of string yaml",required=True)
    
    args = parser.parse_args()
    # phase args end
    try:
        pass # TODO: load config.yaml here