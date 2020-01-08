# PingPong Project Machine-learning

# Requirements
* above Memory 4G
* above Windows 7 operating system
* python 3.7
* Anaconda 1.9.7
# Usage
終端機執行遊戲：
* python MLGame.py [options] pingpong [game_over_score]
* option 可指定遊戲運行的方式，利用 python MLGame.py –h 查看可用的選項
* game_over_score ：指定遊戲結束的分數，當任一方達到此分數，就會結束遊戲。預設是 3 分。

手動執行乒乓球指令：
* python MLGame.py -m pingpong

機器學習模式中的手動模式執行乒乓球指令：
* python MLGame.py pingpong -i ml_play_template.py ml_play_manual.py
* ml_play_template.py 是機器學習的檔案
* ml_play_manual.py 是手動模式的檔案

# Machine Learning Mode
* 乒乓球系統圖

![image](https://github.com/BBS86x1023/PingPong-project-management-of-Machine-learning/blob/master/picture/%E7%B3%BB%E7%B5%B1%E5%9C%96.png)

* 乒乓球MLP訓練流程圖

![image](https://github.com/BBS86x1023/PingPong-project-management-of-Machine-learning/blob/master/picture/%E4%B9%92%E4%B9%93%E7%90%83MLP%E8%A8%93%E7%B7%B4%E6%B5%81%E7%A8%8B%E5%9C%96.png)

# References Link
* MLP：https://github.com/gonzalofrancoceballos/MLP
* PingPong game：https://github.com/LanKuDot/MLGame?fbclid=IwAR26qr0c0YhYf_FQCJcbLbSTr37L069tyZbRrPq3ewI64Io3z_nT9Al61nU
