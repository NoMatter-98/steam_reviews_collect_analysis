# how to use?

(1)Activate environment

./.venv/Scripts/activate

(2)run collector 

python steam_review_collect_black_myth_wukong.py


You will get : "black_myth_wukong_steam_reviews_all.csv" ----Since github can only upload files which is <100MB, here I cut off some rows from original csv.


(3)run analyser

python steam_review_analizer.py


You will get pictures in ./figs


(4)get 300 samples from all reviews, filtering Simple Chinese, and samplize by month portion

python black_myth_sample300.py


You will get "black_myth_wukong_steam_reviews_300_new.csv"
