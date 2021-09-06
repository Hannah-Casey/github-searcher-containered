# github-searcher-containered

This repository contains the containered version of the github search tool used for 'project in computer science' at TU Wien in summer semester 2021. 

In order to download Solidity smart contracts from GitHub using the containered version of the github searcher, the following command is useful: 
```
docker run -d -v ${PWD}\output:/var/log/output  githubsearchercontainered:latest --stratum-size 100 --github-token "XXXXXXXXXXXXXXXXXXXXXXXXXXX" --database res.db --statistics stats.csv "\extension:sol"
```

Of course, the github-token must first be generated and the Xs in the command replaced. 
