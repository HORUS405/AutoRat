#!/bin/bash
sudo apt install snap 
go get -u github.com/tomnomnom/httprobe
GO111MODULE=on go get -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder
sudo snap install amass
#install aquatone

