"""
Python file that help customers to build their JSON structure per platform.
It based on 'PlatformJsonInputExamples' folder.
"""

from API.finvizAPI.finviz import Screener

def main():
    all_available_filters = Screener.load_filter_dict()
    print(all_available_filters)

if __name__ == '__main__':
    main()

