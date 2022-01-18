#!/bin/bash

rm -f *.root
rm -f *.json
rm -f *.txt

cp 2016_muon_900_FWP_btag/muon_2016_900.txt .
cp 2017_muon_900_FWP_btag/muon_2017_900.txt .
cp 2018_muon_900_FWP_btag/muon_2018_900.txt .

cp 2016_electron_900_FWP_btag/ele_2016_900.txt .
cp 2017_electron_900_FWP_btag/ele_2017_900.txt .
cp 2018_electron_900_FWP_btag/ele_2018_900.txt .

cp 2016_muon_750_900_FWP_btag/muon_2016_750_900.txt .
cp 2017_muon_750_900_FWP_btag/muon_2017_750_900.txt .
cp 2018_muon_750_900_FWP_btag/muon_2018_750_900.txt .

cp 2016_electron_750_900_FWP_btag/ele_2016_750_900.txt .
cp 2017_electron_750_900_FWP_btag/ele_2017_750_900.txt .
cp 2018_electron_750_900_FWP_btag/ele_2018_750_900.txt .

combineCards.py muon_2018_900=muon_2018_900.txt  muon_2017_900=muon_2017_900.txt  muon_2016_900=muon_2016_900.txt ele_2018_900=ele_2018_900.txt  ele_2017_900=ele_2017_900.txt ele_2016_900=ele_2016_900.txt  muon_2018_750_900=muon_2018_750_900.txt  muon_2017_750_900=muon_2017_750_900.txt muon_2016_750_900=muon_2016_750_900.txt  ele_2018_750_900=ele_2018_750_900.txt ele_2017_750_900=ele_2017_750_900.txt ele_2016_750_900=ele_2016_750_900.txt > Ac_750.txt

combineCards.py muon_2018_750_900=muon_2018_750_900.txt  muon_2017_750_900=muon_2017_750_900.txt muon_2016_750_900=muon_2016_750_900.txt  ele_2018_750_900=ele_2018_750_900.txt ele_2017_750_900=ele_2017_750_900.txt ele_2016_750_900=ele_2016_750_900.txt > Ac_750_900.txt

combineCards.py muon_2018_900=muon_2018_900.txt  muon_2017_900=muon_2017_900.txt  muon_2016_900=muon_2016_900.txt ele_2018_900=ele_2018_900.txt  ele_2017_900=ele_2017_900.txt ele_2016_900=ele_2016_900.txt > Ac_900.txt

combineCards.py muon_2018_900=muon_2018_900.txt  muon_2017_900=muon_2017_900.txt  muon_2016_900=muon_2016_900.txt muon_2018_750_900=muon_2018_750_900.txt  muon_2017_750_900=muon_2017_750_900.txt muon_2016_750_900=muon_2016_750_900.txt > Ac_muon.txt

combineCards.py ele_2018_900=ele_2018_900.txt  ele_2017_900=ele_2017_900.txt ele_2016_900=ele_2016_900.txt ele_2018_750_900=ele_2018_750_900.txt ele_2017_750_900=ele_2017_750_900.txt ele_2016_750_900=ele_2016_750_900.txt > Ac_ele.txt

text2workspace.py Ac_750.txt -o Ac_750.root  -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel -m 125 --PO map='.*/Ttbar_1:r_neg[1,0,20]' --PO map='.*/Ttbar_2:r_pos=expr;;r_pos("68351/69410*@0*(100+@1)/(100-@1)",r_neg,Ac[-2,-5,0])' --PO verbose 
 
text2workspace.py Ac_900.txt -o Ac_900.root  -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel -m 125 --PO map='.*/Ttbar_1:r_neg[1,0,20]' --PO map='.*/Ttbar_2:r_pos=expr;;r_pos("36099/36764*@0*(100+@1)/(100-@1)",r_neg,Ac[-2,-5,0])' --PO verbose


text2workspace.py Ac_750_900.txt -o Ac_750_900.root  -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel -m 125 --PO map='.*/Ttbar_1:r_neg[1,0,20]' --PO map='.*/Ttbar_2:r_pos=expr;;r_pos("32252/32646*@0*(100+@1)/(100-@1)",r_neg,Ac[-2,-5,0])' --PO verbose

text2workspace.py Ac_muon.txt -o Ac_muon.root  -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel -m 125 --PO map='.*/Ttbar_1:r_neg[1,0,20]' --PO map='.*/Ttbar_2:r_pos=expr;;r_pos("53446/54239*@0*(100+@1)/(100-@1)",r_neg,Ac[-2,-5,0])' --PO verbose

text2workspace.py Ac_ele.txt -o Ac_ele.root  -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel -m 125 --PO map='.*/Ttbar_1:r_neg[1,0,20]' --PO map='.*/Ttbar_2:r_pos=expr;;r_pos("14905/15171*@0*(100+@1)/(100-@1)",r_neg,Ac[-2,-5,0])' --PO verbose


bash impacts_750.sh
mv Ac.pdf Ac_750.pdf 
mv r_neg.pdf r_neg_750.pdf 

bash impacts_750_900.sh
mv Ac.pdf Ac_750_900.pdf
mv r_neg.pdf r_neg_750_900.pdf

bash impacts_900.sh
mv Ac.pdf Ac_900.pdf
mv r_neg.pdf r_neg_900.pdf

bash impacts_muon.sh
mv Ac.pdf Ac_muon.pdf
mv r_neg.pdf r_neg_muon.pdf

bash impacts_ele.sh
mv Ac.pdf Ac_ele.pdf
mv r_neg.pdf r_neg_ele.pdf








 







