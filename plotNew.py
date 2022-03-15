#!/usr/bin/env python
import ROOT
import math
import json
import argparse
import CombineHarvester.CombineTools.plotting as plot
import CombineHarvester.CombineTools.combine.rounding as rounding
from ROOT import *
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.AddDirectory(0)

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', help='input json file')
parser.add_argument('--output', '-o', help='name of the output file to create')
parser.add_argument('--translate', '-t', help='JSON file for remapping of parameter names')
parser.add_argument('--units', default=None, help='Add units to the best-fit parameter value')
parser.add_argument('--per-page', type=int, default=30, help='Number of parameters to show per page')
parser.add_argument('--max-pages', type=int, default=None, help='Maximum number of pages to write')
parser.add_argument('--height', type=int, default=600, help='Canvas height, in pixels')
parser.add_argument('--left-margin', type=float, default=0.4, help='Left margin, expressed as a fraction')
parser.add_argument('--label-size', type=float, default=0.021, help='Parameter name label size')
parser.add_argument('--cms-label', default='Internal', help='Label next to the CMS logo')
parser.add_argument('--transparent', action='store_true', help='Draw areas as hatched lines instead of solid')
parser.add_argument('--checkboxes', action='store_true', help='Draw an extra panel with filled checkboxes')
parser.add_argument('--blind', action='store_true', help='Do not print best fit signal strength')
parser.add_argument('--color-groups', default=None, help='Comma separated list of GROUP=COLOR')
parser.add_argument("--pullDef",  default=None, help="Choose the definition of the pull, see HiggsAnalysis/CombinedLimit/python/calculate_pulls.py for options")
parser.add_argument('--POI', default=None, help='Specify a POI to draw')
args = parser.parse_args()



#c1 = TCanvas("canvas","test",1000,1000);

#TH1F *hr = pad->DrawFrame(0.74,1.74,0.9,1.95);
#pad->GetFrame()->SetFillColor(0);
if args.transparent:
    print 'plotImpacts.py: --transparent is now always enabled, the option will be removed in a future update'

externalPullDef = False
if args.pullDef is not None:
    externalPullDef = True
    import HiggsAnalysis.CombinedLimit.calculate_pulls as CP


def Translate(name, ndict):
    return ndict[name] if name in ndict else name


def GetRounded(nom, e_hi, e_lo):
    if e_hi < 0.0:
        e_hi = 0.0
    if e_lo < 0.0:
        e_lo = 0.0
    rounded = rounding.PDGRoundAsym(nom, e_hi if e_hi != 0.0 else 1.0, e_lo if e_lo != 0.0 else 1.0)
    s_nom = rounding.downgradePrec(rounded[0],rounded[2])
    s_hi = rounding.downgradePrec(rounded[1][0][0],rounded[2]) if e_hi != 0.0 else '0'
    s_lo = rounding.downgradePrec(rounded[1][0][1],rounded[2]) if e_lo != 0.0 else '0'
    return (s_nom, s_hi, s_lo)
#f=open("prefit_unc.json","r")
#data1 = json.load(f)
#f.close()
# Dictionary to translate parameter names
translate = {}
if args.translate is not None:
    with open(args.translate) as jsonfile:
        translate = json.load(jsonfile)
#	translate2= json.load("prefit_vals.json")
# Load the json output of combineTool.py -M Impacts
data = {}
with open(args.input) as jsonfile:
    data = json.load(jsonfile)

# Set the global plotting style
plot.ModTDRStyle(l=args.left_margin, b=0.10, width=(900 if args.checkboxes else 700), height=args.height)
#prefit_vals={"Q2 #mu_{R}(down) #mu_{F}(down)":[0.15,0.15],"FSR":[1.0,1.0],"Top-tag":[0.01,0.01],"btag (LF corr)":[0.01,0.01],"btag (HF unc 2018)":[0.01,0.01],"btag (HF corr)":[0.01,0.01], "Top p_{T} reweight":[0.001,0.05],"Ele HLT":[0.08,0.08],"hdamp":[1.,1.],"Q2 #mu_{R}(down) #mu_{F}(central)":[0.15,0.001],"Q2 #mu_{R}(down) #mu_{F}(down)":[0.22,0.001],"Q2 #mu_{R}(up) #mu_{F}(central)":[0.001,0.14],"Q2 #mu_{R}(up) #mu_{F}(up)":[0.16,0.16],"Q2 #mu_{R}(down) #mu_{F}(central)":[0.16,0.16],"Mu HLT":[1.,1.],"Mu ID":[1.,1.], "Mu Reco":[1.,1.],"Ele ID":[1.,1.],"JEC AbsoluteStat":[1.,1.] ,"JEC RelativeJEREC1":[1.,1.], "JEC RelativeJEREC2":[1.,1.], "JEC RelativePtEC1":[1.,1.],"JEC RelativePtEC2":[1.,1.], "JEC RelativeSample":[1.,1.],"JEC RelativeStatEC":[1.,1.] ,"JEC RelativeStatFSR":[1.,1.] , "JEC RelativeStatHF":[1.,1.], "JEC TimePtEta":[1.,1.],"TTbar xsec":[0.05,0.05],"QCD xsec":[0.5,0.5],"SingleTop xsec":[.3,.3],"WJets xsec":[.3,.3],"JER":[1.,1.],"PDF_32":[0.01,0.01],"PDF_67":[0.01,0.01],"luminosity (2016)":[0.025,0.025],"luminosity (2017)":[0.023,0.023], "btag (HF unc 2016)":[0.01,0.01], "ISR":[1.0,1.0],}
# We will assume the first POI is the one to plot
prefit_vals={"PDF_33":[1.,1.],"PDF_12":[1.,1.],"PDF_10":[1.,1.],"PDF_24":[1.,1.],"luminosity_1718":[0.6,0.6],"btag_HF_unc17":[0.01,0.01],"luminosity_2018":[0.025,0.025],"q2MuRctMuFup":[0.16,0.16],"q2MuRctMuFdn":[0.16,0.16],"PDF_50":[0.01,0.01],"jer":[1.,1.],"btag_HF_unc18":[0.01,0.01],"jectimepteta":[1.,1.],"PDF_56":[1.,1.],"q2MuRdnMuFdn":[0.22,0.001],"FSR":[1.0,1.0],"toptag":[0.01,0.01],"btag_LF_corr":[0.01,0.01],"btag_HF_unc18)":[0.01,0.01],"btag_HF_corr":[0.01,0.01], "Top_pT_rew":[0.001,0.05],"eleHLT":[0.08,0.08],"hdamp":[1.,1.],"q2MuRdnMuFct":[0.15,0.001],"q2MuRupMuFct":[0.001,0.14],"q2MuRupMuFup":[0.16,0.16],"q2MuRdnMuFct":[0.16,0.16],"muHLT":[1.,1.],"muID":[1.,1.], "mu_reco":[1.,1.],"eleID":[1.,1.],"jecAbsoluteStat":[1.,1.] ,"jecRelativeJEREC1":[1.,1.], "jecRelativeJEREC2":[1.,1.], "jecRelativePtEC1":[1.,1.],"jecRelativePtEC2":[1.,1.], "jecRelativeSample":[1.,1.],"jecRelativeStatEC":[1.,1.] ,"jecRelativeStatFSR":[1.,1.] , "jecRelativeStatHF":[1.,1.], "jecTimePtEta":[1.,1.],"xsec_Ttbar":[0.05,0.05],"xsec_qcd":[0.5,0.5],"xsec_singletop":[.3,.3],"xsec_wjets":[.3,.3],"jer":[1.,1.],"PDF_32":[0.01,0.01],"PDF_67":[0.01,0.01],"luminosity_2016":[0.025,0.025],"luminosity_2017":[0.023,0.023], "btag_HF_unc16":[0.01,0.01], "ISR":[1.0,1.0],}
 


POIs = [ele['name'] for ele in data['POIs']]
POI = POIs[0]
if args.POI:
    POI = args.POI

for ele in data['POIs']:
    if ele['name'] == POI:
        POI_info = ele
        break

POI_fit = POI_info['fit']
#for inter in data['params']:
#	print inter['name']
	#for what in inter:
	#	print inter['name']

#sys.exit()
# Sort parameters by largest absolute impact on this POI
data['params'].sort(key=lambda x: abs(x['impact_%s' % POI]), reverse=True)
print len(data['params'])
#for i in range(len(data['params'])):
#	print i
#	print i, data['params'][i]
#	if 'prop_' in data['params'][i]['name']:
#		data['params'].pop(i)

#print data['params']
#print len(data['params'])
		
if args.checkboxes:
    cboxes = data['checkboxes']

# Set the number of parameters per page (show) and the number of pages (n)
show = args.per_page
n = int(math.ceil(float(len(data['params'])) / float(show)))
if args.max_pages is not None and args.max_pages > 0:
    n = args.max_pages

colors = {
    'Gaussian': 1,
    'Poisson': 8,
    'AsymmetricGaussian': 9,
    'Unconstrained': 39,
    'Unrecognised': 2
}
color_hists = {}
color_group_hists = {}

if args.color_groups is not None:
    color_groups = {
        x.split('=')[0]: int(x.split('=')[1]) for x in args.color_groups.split(',')
    }

seen_types = set()

for name, col in colors.iteritems():
    color_hists[name] = ROOT.TH1F()
    plot.Set(color_hists[name], FillColor=col, Title=name)

if args.color_groups is not None:
    for name, col in color_groups.iteritems():
        color_group_hists[name] = ROOT.TH1F()
        plot.Set(color_group_hists[name], FillColor=col, Title=name)

for page in xrange(n):
   # if ('prop_' in data['params']['name']):continue
    
    canv = ROOT.TCanvas(args.output, args.output)
    n_params = len(data['params'][show * page:show * (page + 1)])
    pdata = data['params'][show * page:show * (page + 1)]
    print '>> Doing page %i, have %i parameters' % (page, n_params)

    boxes = []
    for i in xrange(n_params):
#	if ('prop_' in pdata[i]['name']):continue
        y1 = ROOT.gStyle.GetPadBottomMargin()
        y2 = 1. - ROOT.gStyle.GetPadTopMargin()
        h = (y2 - y1) / float(n_params)
        y1 = y1 + float(i) * h
        y2 = y1 + h
        box = ROOT.TPaveText(0, y1, 1, y2, 'NDC')
        plot.Set(box, TextSize=0.02, BorderSize=0, FillColor=0, TextAlign=12, Margin=0.005)
        if i % 2 == 0:
            box.SetFillColor(18)
        box.AddText('%i' % (n_params - i + page * show))
        box.Draw()
        boxes.append(box)

    # Crate and style the pads
 #   if args.checkboxes:
#        pads = plot.MultiRatioSplitColumns([0.54, 0.24], [0., 0.], [0., 0.])
#	pads=plot.OnePad()
 #       pads[2].SetGrid(1, 0)
  #  else:
#	pads=plot.OnePad()
    pad = ROOT.TPad('pad', 'pad', 0., 0., 1., 1.)
    pad.SetFillStyle(4000);
    pad.SetFillColor(0);
    pad.SetFrameFillStyle(4000);
    pad.Draw();
    pad.SetTicks(0,0);
    pad.cd();   
      #  pads = plot.MultiRatioSplitColumns([0.7], [0.], [0.])
    pad.SetGrid(1, 0)
    pad.SetTickx(0)

    hframe1=pad.DrawFrame(-2.9,1,2.9,30)
    hframe1.GetXaxis().SetNdivisions(0)
    #pads[1].SetGrid(1, 0)
    #pads[1].SetTickx(1)

    h_pulls = ROOT.TH2F("pulls", "pulls", 6, -2.9, 2.9, n_params, 0, n_params)
    g_pulls = ROOT.TGraphAsymmErrors(n_params)
    g_prepull= ROOT.TGraphAsymmErrors(n_params)
    #g1 = TGaxis(-4.5,-0.2,5.5,-0.2,-2.9,2.9,510,"");
  #  g1.SetName("g1");
    #g1.Draw();
    g_impacts_hi = ROOT.TGraphAsymmErrors(n_params)
    g_impacts_lo = ROOT.TGraphAsymmErrors(n_params)
    #g2=TGaxis(-4.5,-0.2,5.5,-0.2,-0.2,0.2,510,"+");
    #g2.SetName("g2");
    g_check = ROOT.TGraphAsymmErrors()
    g_check_i = 0

    max_impact = 0.

    text_entries = []
    redo_boxes = []
    for p in xrange(n_params):
#	if ('prop_' in pdata[p]['name']):continue
        i = n_params - (p + 1)
        pre = pdata[p]['prefit']
        fit = pdata[p]['fit']
        tp = pdata[p]['type']
        seen_types.add(tp)
        if pdata[p]['type'] != 'Unconstrained':
            pre_err_hi = (pre[2] - pre[1])
            pre_err_lo = (pre[1] - pre[0])

            if externalPullDef:
                fit_err_hi = (fit[2] - fit[1])
                fit_err_lo = (fit[1] - fit[0])
                pull, pull_hi, pull_lo = CP.returnPullAsym(args.pullDef,fit[1],pre[1],fit_err_hi,pre_err_hi,fit_err_lo,pre_err_lo)
            else:
                pull = fit[1] - pre[1]
                pull = (pull/pre_err_hi) if pull >= 0 else (pull/pre_err_lo)
                pull_hi = fit[2] - pre[1]
                pull_hi = (pull_hi/pre_err_hi) if pull_hi >= 0 else (pull_hi/pre_err_lo)
                pull_hi = pull_hi - pull
                pull_lo = fit[0] - pre[1]
                pull_lo = (pull_lo/pre_err_hi) if pull_lo >= 0 else (pull_lo/pre_err_lo)
                pull_lo =  pull - pull_lo
	#    print prefit_vals[pdata[p]['name']], pdata[p]['name']	
            if (prefit_vals[pdata[p]['name']][0]==1. or prefit_vals[pdata[p]['name']][1]==1.):
            	prepull_hi=1.
                prepull_lo=1.
            else:
            
            	prepull_hi=1+prefit_vals[pdata[p]['name']][0]*1.
            
            	prepull_lo=1-prefit_vals[pdata[p]['name']][1]*1.
            
    #        print i, pdata[p]['name'], prepull_hi, prepull_hi
     #       print i, pdata[p]['name'], pull_lo, prepull_hi
            g_pulls.SetPoint(i, pull, float(i) + 0.5)
            g_prepull.SetPoint(i,0.,float(i) + 0.5)
           
            g_pulls.SetPointError(i, pull_lo, pull_hi, 0., 0.)
            g_prepull.SetPointError(i,prepull_lo, prepull_hi,0.5,0.5)
        else:
            # Hide this point
            g_pulls.SetPoint(i, 0., 9999.)
            y1 = ROOT.gStyle.GetPadBottomMargin()
            y2 = 1. - ROOT.gStyle.GetPadTopMargin()
            x1 = ROOT.gStyle.GetPadLeftMargin()
            h = (y2 - y1) / float(n_params)
            y1 = y1 + ((float(i)+0.5) * h)
            x1 = x1 + (1 - pads[0].GetRightMargin() -x1)/2.
            s_nom, s_hi, s_lo = GetRounded(fit[1], fit[2] - fit[1], fit[1] - fit[0])
            text_entries.append((x1, y1, '%s^{#plus%s}_{#minus%s}' % (s_nom, s_hi, s_lo)))
            redo_boxes.append(i)
        g_impacts_hi.SetPoint(i, 0, float(i) + 0.5)
        g_impacts_lo.SetPoint(i, 0, float(i) + 0.5)
        if args.checkboxes:
            pboxes = pdata[p]['checkboxes']
            for pbox in pboxes:
                cboxes.index(pbox)
                g_check.SetPoint(g_check_i, cboxes.index(pbox) + 0.5, float(i) + 0.5)
                g_check_i += 1
        imp = pdata[p][POI]
       
        g_impacts_hi.SetPointError(i, 0, imp[2] - imp[1], 0.5, 0.5)
        g_impacts_lo.SetPointError(i, imp[1] - imp[0], 0, 0.5, 0.5)
        #print i, pdata[p]['name'], imp[2] - imp[1], imp[1] - imp[0]
        max_impact = max(
            max_impact, abs(imp[1] - imp[0]), abs(imp[2] - imp[1]))
        col = colors.get(tp, 2)
        if args.color_groups is not None and len(pdata[p]['groups']) >= 1:
            for p_grp in pdata[p]['groups']:
                if p_grp in color_groups:
                    col = color_groups[p_grp]
                    break
	print i
	print "check:",col, Translate(pdata[p]['name'],translate), translate
        h_pulls.GetYaxis().SetBinLabel(
            i + 1, ('#color[%i]{%s}'% (col, Translate(pdata[p]['name'], translate))))


    #h_pulls.Draw()
    #canv.SaveAs("check_h_pull.pdf")


    # Style and draw the pulls histo
    if externalPullDef:
        plot.Set(h_pulls.GetXaxis(), TitleSize=0.04, LabelSize=0.03, Title=CP.returnTitle(args.pullDef))
    else:
        plot.Set(h_pulls.GetXaxis(), TitleSize=0.04, LabelSize=0.03, Title='(#hat{#theta}-#theta_{0})/#Delta#theta')

    plot.Set(h_pulls.GetYaxis(), LabelSize=args.label_size, TickLength=0.0)
    h_pulls.GetYaxis().LabelsOption('v')
  #  canv.cd()
    h_pulls.Draw()
    #canv.SaveAs("check_h_pull_2.pdf")
    for i in redo_boxes:
        newbox = boxes[i].Clone()
        newbox.Clear()
        newbox.SetY1(newbox.GetY1()+0.005)
        newbox.SetY2(newbox.GetY2()-0.005)
        newbox.SetX1(ROOT.gStyle.GetPadLeftMargin()+0.001)
        newbox.SetX2(0.7-0.001)
        newbox.Draw()
        boxes.append(newbox)
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.SetTextSize(0.02)
    latex.SetTextAlign(22)
    for entry in text_entries:
        latex.DrawLatex(*entry)

    # Go to the other pad and draw the impacts histo
    pad.cd()
    if max_impact == 0.: max_impact = 1E-6  # otherwise the plotting gets screwed up
    h_impacts = ROOT.TH2F(
        "impacts", "impacts", 6, -max_impact * 1.1, max_impact * 1.1, n_params, 0, n_params)
    plot.Set(h_impacts.GetXaxis(), LabelSize=0.03, TitleSize=0.04, Ndivisions=505, Title=
        '#Delta#hat{%s}' % (Translate(POI, translate)))
    plot.Set(h_impacts.GetYaxis(), LabelSize=0, TickLength=0.0)
   # h_impacts.Draw("")
    #canv.SaveAs("check_h_impacts.pdf")
    if args.checkboxes:
        pads[2].cd()
        h_checkboxes = ROOT.TH2F(
            "checkboxes", "checkboxes", len(cboxes), 0, len(cboxes), n_params, 0, n_params)
        for i, cbox in enumerate(cboxes):
            h_checkboxes.GetXaxis().SetBinLabel(i+1, Translate(cbox, translate))
        plot.Set(h_checkboxes.GetXaxis(), LabelSize=0.03, LabelOffset=0.002)
        h_checkboxes.GetXaxis().LabelsOption('v')
        plot.Set(h_checkboxes.GetYaxis(), LabelSize=0, TickLength=0.0)
        h_checkboxes.Draw()

    # Back to the first pad to draw the pulls graph
   # pads[0].cd()
 #   plot.Set(g_pulls, MarkerSize=0.8, LineWidth=2)
#    g_pulls.Draw('PSAME')

    # And back to the second pad to draw the impacts graphs
    #pads[0].cd()
    #plot.Set(g_pulls, MarkerSize=0.8, LineWidth=2)
    g_pulls.Draw('PSAME')
    #g_prepull.GetAttLine(1).SetLineColor(kGreen)
    g_prepull.SetLineColor(31)
    g_prepull.SetFillColorAlpha(0,0.15)
    #g_prepull.SetFillStyle(3004)
    g_prepull.Draw('5SAME')
    #c1.SaveAs("check.pdf")
    alpha = 0.7
    canv.cd()
    pad1 = ROOT.TPad('pad1', 'pad1', 0., 0., 1., 1.) 
    pad1.SetFillStyle(4000);
    pad1.SetFillColor(0);
    pad1.SetFrameFillStyle(4000);
    pad1.Draw();
    pad1.SetTicks(0,0);
    pad1.cd();
    hframe2=pad1.DrawFrame(-0.2,1,0.2,30)
    hframe2.GetXaxis().SetNdivisions(0)
    hframe2.GetYaxis().SetNdivisions(0)
    
    lo_color = {
        'default': 38,
        'hesse': ROOT.kOrange - 3,
        'robust': ROOT.kGreen + 1
    }
    hi_color = {
        'default': 46,
        'hesse': ROOT.kBlue,
        'robust': ROOT.kAzure - 5
    }
    method = 'default'
    if 'method' in data and data['method'] in lo_color:
        method = data['method']
    g_impacts_hi.GetXaxis().SetTickLength(0)
    g_impacts_lo.GetXaxis().SetTickLength(0) 
    g_impacts_hi.SetFillColor(plot.CreateTransparentColor(hi_color[method], alpha))
    #g_impacts_hi.Draw('2SAME')
    g_impacts_lo.SetFillColor(plot.CreateTransparentColor(lo_color[method], alpha))
    #g_impacts_lo.Draw('2SAME')
    g1 = TGaxis(-0.2,30,0.2,30,-0.2,0.2,510,"-");
    g1.SetLabelSize(0.03)
    g1.SetLabelFont(42)
    g1.Draw("same")
  #  g2.Draw("same")
    #canv.Update()
    #canv.Print('check.pdf')
    #pads[0].RedrawAxis()
    
    legend = ROOT.TLegend(0.02, 0.02, 0.40, 0.06, '', 'NBNDC')
    legend.SetNColumns(3)
    legend.AddEntry(g_pulls, 'Pull', 'LP')
    legend.AddEntry(g_impacts_hi, '+1#sigma Impact', 'F')
    legend.AddEntry(g_impacts_lo, '-1#sigma Impact', 'F')
    legend.AddEntry(g_prepull, 'Prefit fit uncertainty', 'F')
    legend.Draw()

    leg_width = pad.GetLeftMargin() - 0.01
    if args.color_groups is not None:
        legend2 = ROOT.TLegend(0.01, 0.94, leg_width, 0.99, '', 'NBNDC')
        legend2.SetNColumns(2)
        for name, h in color_group_hists.iteritems():
            legend2.AddEntry(h, Translate(name, translate), 'F')
        legend2.Draw()
    elif len(seen_types) > 1:
        legend2 = ROOT.TLegend(0.01, 0.94, leg_width, 0.99, '', 'NBNDC')
        legend2.SetNColumns(2)
        for name, h in color_hists.iteritems():
            if name == 'Unrecognised': continue
            legend2.AddEntry(h, name, 'F')
        legend2.Draw()
    pt = TPaveText(0.01,.93,0.1,.98,"NBNDC")
    pt.AddText("CMS");
    pt.SetFillColorAlpha(0,0.15)
    pt.SetTextFont(62)
    pt.Draw()
    s_nom, s_hi, s_lo = GetRounded(POI_fit[1], POI_fit[2] - POI_fit[1], POI_fit[1] - POI_fit[0])
    pt1 = TPaveText(0.2,.93,0.3,.98,"NBNDC")
    pt1.SetFillColorAlpha(0,0.15)
    print Translate(POI, translate), s_nom, s_hi, s_lo
    pt1.AddText('#hat{%s} = %s^{#plus%s}_{#minus%s}' % ( Translate(POI, translate), s_nom, s_hi, s_lo))
           # '' if args.units is None else ' '+args.units), 3, 0.27)
    pt1.SetTextFont(42)
    pt1.Draw()
    #plot.DrawCMSLogo(pad1, 'CMS', "", 0.001, 0, 0.0, 0.00)
    s_nom, s_hi, s_lo = GetRounded(POI_fit[1], POI_fit[2] - POI_fit[1], POI_fit[1] - POI_fit[0])
   # if not args.blind:
    #    plot.DrawTitle(pad, '#hat{%s} = %s^{#plus%s}_{#minus%s}%s' % (
     #       Translate(POI, translate), s_nom, s_hi, s_lo,
      #      '' if args.units is None else ' '+args.units), 3, 0.27)
    extra = ''
    if page == 0:
        extra = '('
    if page == n - 1:
        extra = ')'
    canv.Print('.pdf%s' % extra)
