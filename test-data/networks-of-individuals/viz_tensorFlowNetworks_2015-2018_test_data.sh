echo -e "vizualize test data"

#echo  checking ScrapLog is on last version
#(cd  ../../../ScrapLogGit2Net/ && git pull)

echo calling the visualizers for each file

../../../ScrapLogGit2Net/formatFilterAndViz-nofi-GraphML.py -lp tensorFlowGitLog-2016-git-log-outpuyt-by-Jose.IN.NetworkFile.graphML
../../../ScrapLogGit2Net/formatFilterAndViz-nofi-GraphML.py -lp tensorFlowGitLog-2017-git-log-outpuyt-by-Jose.IN.NetworkFile.graphML
../../../ScrapLogGit2Net/formatFilterAndViz-nofi-GraphML.py -lp tensorFlowGitLog-2018-git-log-outpuyt-by-Jose.IN.NetworkFile.graphML
