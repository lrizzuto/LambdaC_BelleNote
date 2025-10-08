import ROOT
import parameters


newfile = 'stream0_Total_fit_chargedControlD0_rel5.root'

file = ROOT.TFile.Open(newfile)
mc = ROOT.TChain('Tree')
mc.Add(newfile)
 
mbc = ROOT.RooRealVar("Mbc","M_{bc} (GeV/c^{2})",5.25,5.29)
InvM = ROOT.RooRealVar("InvM","M_{K #pi} (GeV/c^{2})",1.8, 1.93)



df = ROOT.RooDataSet('df','df', ROOT.RooArgSet(mbc,InvM))
for i in range(mc.GetEntries()):
	mc.GetEntry(i)
	if 	mc.Mbc > 5.25 and mc.InvM > 1.80 and mc.InvM < 1.93:
		mbc.setVal(mc.Mbc)
		InvM.setVal(mc.InvM)
		df.add(ROOT.RooArgSet(mbc,InvM))
print("proceeding with the fit on stream0 ...with number of entries: " )

print("                            ")
df.Print("v")

####===============####
#### Mbc Fit Model:   #
####===============####




###
##Total Signal Mbc Fit Model:
###========================###


##CB1 for signal
alpha1 = ROOT.RooRealVar('alpha1','alpha1', parameters.alpha1)# 2.19418)#
mB1 = ROOT.RooRealVar('mB1','mB1', parameters.mB1)#5.27908)#
n1 = ROOT.RooRealVar('n1','n1', parameters.n1)
sigmaCB1 = ROOT.RooRealVar('sigmaCB1','sigmaCB1', parameters.sigmaCB1, 0.0005, 0.01)

signalCB = ROOT.RooCBShape('signalCB','signalCB', mbc,mB1,sigmaCB1,alpha1,n1)



#Novosibirsk for mis-reconstructed signal events
Sigbkg_peak = ROOT.RooRealVar('Sigbkg_peak', 'bkg_peak', parameters.peak)
Sigbkg_sigma = ROOT.RooRealVar('Sigbkg_sigma','width', parameters.sigma)
Sigbkg_k = ROOT.RooRealVar('Sigbkg_k','tail', parameters.k)

SigBkg_Novosibirsk = ROOT.RooNovosibirsk('SigBkg_Novosibirsk', 'Novosibirsk pdf', mbc, Sigbkg_peak, Sigbkg_sigma, Sigbkg_k)


###===============
#Generic:
####===============####

alpha2 = ROOT.RooRealVar('alpha2','alpha', parameters.alpha2)#6.89949e-01, 0.1, 10)
mB2 = ROOT.RooRealVar('mB2','mB2', parameters.mB2)# , 5.275, 5.285)#) #           "            "
n2 = ROOT.RooRealVar('n2','n2', parameters.n2)
sigma_r2 = ROOT.RooRealVar("Sigma r. of generic CB","sigma3/sigma1", parameters.Sigma_ratio)

sigmaCB2 = ROOT.RooProduct("sigmaCB3","width of gaussian 3",ROOT.RooArgList(sigmaCB1,sigma_r2))

CB2 = ROOT.RooCBShape('CB2','CB2',mbc,mB2,sigmaCB2,alpha2,n2)

#Generic Novosibirsk:
Generic_peak = ROOT.RooRealVar('Generic_peak', 'Generic_peak', parameters.Generic_peak)#, 5.26, 5.29)
Generic_sigma = ROOT.RooRealVar('Generic_sigma','width', parameters.Generic_sigma)#, 0.01, 0.1)
Generic_tail = ROOT.RooRealVar('Generic_tail','k', parameters.Generic_tail)#, 0.1, 20)

Generic_Novosibirsk = ROOT.RooNovosibirsk('Generic_Novosibirsk', 'Novosibirsk pdf', mbc, Generic_peak, Generic_sigma, Generic_tail)

frac_mbc = ROOT.RooRealVar('frac_mbc','frac_mbc', parameters.generic_frac_mbc)

Generic_Mbc = ROOT.RooAddPdf('Generic_Mbc','',ROOT.RooArgList(CB2,Generic_Novosibirsk),ROOT.RooArgList(frac_mbc))

###===============
## Neutral-crossfeed
###==============

Crossfeed_peak = ROOT.RooRealVar('Crossfeed_peak', 'Crossfeed_peak', parameters.Crossfeed_peak)
Crossfeed_sigma = ROOT.RooRealVar('Crossfeed_sigma','width', parameters.Crossfeed_sigma)
Crossfeed_k = ROOT.RooRealVar('Crossfeed_k','tail', parameters.Crossfeed_tail)

Crossfeed_Novosibirsk = ROOT.RooNovosibirsk('Crossfeed_Novosibirsk', 'Novosibirsk pdf', mbc, Crossfeed_peak, Crossfeed_sigma, Crossfeed_k)

mArg3 = ROOT.RooRealVar('mArg3','mArg3', parameters.Crossfeed_mArg)
cArg3 = ROOT.RooRealVar('cArg3','cArg3', parameters.Crossfeed_cArg)
neutral_argus = ROOT.RooArgusBG('neutral_argus','neutral_argus',mbc,mArg3,cArg3)

NeutralMbcfrac = ROOT.RooRealVar('NeutralMbcfrac','frac_mbc', parameters.Crossfeed_frac_mbc)

neutralMbc = ROOT.RooAddPdf("neutralMbc_pdf", "neutralMbc pdf", ROOT.RooArgList(Crossfeed_Novosibirsk, neutral_argus), ROOT.RooArgList(NeutralMbcfrac))

####===============####
#### Mbc Continuum Fit Model:   #
####===============####

Continuum_peak = ROOT.RooRealVar('Continuum_peak', 'Continuum_peak', parameters.Continuum_peak)
Continuum_sigma = ROOT.RooRealVar('Continuum_sigma','width', parameters.Continuum_sigma)
Continuum_k = ROOT.RooRealVar('Continuum_k','tail', parameters.Continuum_k)

Continuum_Novosibirsk = ROOT.RooNovosibirsk('Continuum_Novosibirsk', 'Novosibirsk pdf', mbc, Continuum_peak, Continuum_sigma, Continuum_k)


#####
# InvM model
##=====

mean = ROOT.RooRealVar("Mean1", "Mass value", parameters.mean)
sigma1 = ROOT.RooRealVar("Sigma1", "width of gaussian 1", parameters.InvMsigma, 0.006,0.3)
InvMsigma_r1 = ROOT.RooRealVar("InvMSigmaR1","sigma2/sigma1", parameters.InvMSigmaR1)#, 0.006,0.3)
InvMsigma_r2 = ROOT.RooRealVar("InvMSigmaR2","sigma3/sigma1", parameters.InvMSigmaR2)#, 0.006,0.3)
sigma2 = ROOT.RooProduct("Sigma2","width of gaussian 2", ROOT.RooArgList(sigma1,InvMsigma_r1))
sigma3 = ROOT.RooProduct("Sigma3","width of gaussian 3", ROOT.RooArgList(sigma1,InvMsigma_r2))

pdf1 = ROOT.RooGaussian("pdf1","gaussian Signal",InvM,mean,sigma1)
pdf2 = ROOT.RooGaussian("pdf2","gaussian Signal",InvM,mean,sigma2)
pdf3 = ROOT.RooGaussian("pdf3","gaussian Signal",InvM,mean,sigma3)

frac1 = ROOT.RooRealVar("frac1", "frac1", parameters.frac1)
frac2 = ROOT.RooRealVar("frac2", "frac2", parameters.frac2)
InvM_Gauss1 = ROOT.RooAddPdf("InvM_Gauss1", "InvM_Gauss1", ROOT.RooArgList(pdf1, pdf2, pdf3), ROOT.RooArgList(frac1, frac2))
InvM_Gauss2 = ROOT.RooAddPdf("InvM_Gauss2", "InvM_Gauss2", ROOT.RooArgList(pdf1, pdf2, pdf3), ROOT.RooArgList(frac1, frac2))
InvM_Gauss3 = ROOT.RooAddPdf("InvM_Gauss3", "InvM_Gauss3", ROOT.RooArgList(pdf1, pdf2, pdf3), ROOT.RooArgList(frac1, frac2))

SignalInvM_slope = ROOT.RooRealVar("SignalInvM_slope", "SignalInvM_slope InvM slope",  parameters.SignalInvM_slope)#-5.60066e-01)#, -1, 0)
CP0 = ROOT.RooChebychev("CP0", "Chebychev", InvM, ROOT.RooArgList(SignalInvM_slope))
SignalInvM_frac = ROOT.RooRealVar("SignalInvM_frac", "fraction of gauss vs Chebychev", parameters.SignalInvM_frac)

InvM_pdfSig1 = ROOT.RooAddPdf("InvM_pdfSig1", "correct Signal", ROOT.RooArgList(InvM_Gauss1, CP0), ROOT.RooArgList(SignalInvM_frac))
InvM_pdfSig2 = ROOT.RooAddPdf("InvM_pdfSig2", "incompleteB Signal", ROOT.RooArgList(InvM_Gauss2, CP0), ROOT.RooArgList(SignalInvM_frac))
InvM_pdfBkg = ROOT.RooAddPdf("InvM_pdfBkg", "Background", ROOT.RooArgList(InvM_Gauss3, CP0), ROOT.RooArgList(SignalInvM_frac))


#Generic:
a0 = ROOT.RooRealVar("a0", "a0", parameters.a0)

Pol = ROOT.RooPolynomial("Pol","Pol",InvM, ROOT.RooArgList(a0))


###===============
## Neutral-crossfeed
###==============
## NeutralCrossfeed given by Chebychev of first order + the 3 gauss pdf

c0 = ROOT.RooRealVar("NeutralCrossfeed InvM slope", "slope", parameters.c0)
CP1 = ROOT.RooChebychev("CP1", "Chebychev", InvM, ROOT.RooArgList(c0))

Neutral_Gauss = ROOT.RooAddPdf("Neutral_Gauss", "Neutral_Gauss", ROOT.RooArgList(pdf1, pdf2, pdf3), ROOT.RooArgList(frac1, frac2))

neutralInvMfrac = ROOT.RooRealVar("neutralInvMfrac", "fraction of gauss vs Chebychev", parameters.neutralInvMfrac)

InvM_NeutralCrossfeed = ROOT.RooAddPdf("InvM_NeutralCrossfeed", "NeutralCrossfeed", ROOT.RooArgList(Neutral_Gauss, CP1), ROOT.RooArgList(neutralInvMfrac))


#####=========================####
#### InvM Continuum Fit Model:  ##
####==========================####


d0 = ROOT.RooRealVar("d0", "continuum InvM slope", parameters.d0)
CP2 = ROOT.RooChebychev("CP2", "Chebychev", InvM, ROOT.RooArgList(d0))
ccbar_Gauss = ROOT.RooAddPdf("ccbar gauss", "gaussian pdf", ROOT.RooArgList(pdf1, pdf2, pdf3), ROOT.RooArgList(frac1, frac2))
continuumInvMfrac = ROOT.RooRealVar("continuumInvMfrac", "fraction of gauss vs Chebychev", parameters.continuumInvMfrac)
InvM_Continuum = ROOT.RooAddPdf("InvM_Continuum", "Continuum InvM pdf", ROOT.RooArgList(ccbar_Gauss, CP2), ROOT.RooArgList(continuumInvMfrac))


pdfSig1 = ROOT.RooProdPdf('pdfSig1','correct signal 2D pdf',ROOT.RooArgList(signalCB,InvM_pdfSig1))

pdfSig2 = ROOT.RooProdPdf('pdfSig2','incompleteB signal 2D pdf',ROOT.RooArgList(SigBkg_Novosibirsk,InvM_pdfSig2))

pdfGeneric = ROOT.RooProdPdf('pdfGeneric','generic 2D pdf', ROOT.RooArgList(Generic_Mbc, Pol))

NeutralCrossfeed = ROOT.RooProdPdf('NeutralCrossfeed', 'NeutralCrossfeed', ROOT.RooArgList(neutralMbc, InvM_NeutralCrossfeed))

Continuum_pdf = ROOT.RooProdPdf('continuum_pdf','total continuum pdf', ROOT.RooArgList(Continuum_Novosibirsk,InvM_Continuum))


#TotSig = ROOT.RooRealVar('TotSig','total sig events', 78782, 1000, 15000)
NrecSig = ROOT.RooRealVar('NrecSig','total sig events', 5.9e+04, 30000, 120000)
NmisSig = ROOT.RooRealVar('NmisSig','total mis-reco. signal events', 3.6e+04, 10000, 70000)
Ncontinuum = ROOT.RooRealVar('Ncontinuum','total continuum bkg events', 79109)#, 400000, 430000)
Crossfeed_fraction = ROOT.RooRealVar('Crossfeed_fraction','fraction of crossfeed/NmisSig', 0.67719)
N_Crossfeed = ROOT.RooProduct('N_Crossfeed','charged-cross. bkg events', ROOT.RooArgList(NmisSig,Crossfeed_fraction))
N_Generic = ROOT.RooRealVar('N_Generic','N_Generic', 40365, 20000, 80000)

pdf = ROOT.RooAddPdf('pdf','Total pdf', ROOT.RooArgList(pdfSig1, pdfSig2,pdfGeneric, NeutralCrossfeed, Continuum_pdf), ROOT.RooArgList(NrecSig, NmisSig, N_Generic, N_Crossfeed, Ncontinuum))
#TotSig MC = 78583
TotSig = ROOT.RooFormulaVar("tot sig. events", "NrecSig+NmisSig", ROOT.RooArgList(NrecSig,NmisSig))

#Tot MC = 248200
Tot = ROOT.RooFormulaVar("tot normalisation", "NrecSig+NmisSig+N_Generic+N_Crossfeed+Ncontinuum", ROOT.RooArgList(NrecSig, NmisSig,N_Generic,N_Crossfeed,Ncontinuum))

#incompleteB = ROOT.RooFormulaVar("events with Bsig=0", "NmisSig + (1-sig_fraction)*NrecSig", ROOT.RooArgList(NrecSig,sig_frac,NmisSig))

result = pdf.fitTo(df, ROOT.RooFit.Save())


mbc.setRange("Region1", 5.25, 5.29)
InvM.setRange("Region2", 1.80, 1.93)

mbc_frame = df.plotOn(mbc.frame(55))
InvM_frame = df.plotOn(InvM.frame(60))



mbc.setRange("MbcSigR", 5.27, 5.29)
InvM.setRange("InvMSigR", 1.85, 1.88)

mbcSignal_frame = df.plotOn(mbc.frame(45), ROOT.RooFit.CutRange('InvMSigR'))
InvMSignal_frame = df.plotOn(InvM.frame(50), ROOT.RooFit.CutRange('MbcSigR'))

mbc.setRange("Mbc_sidebandwindow2", 5.25, 5.265)
InvM.setRange("InvM_sidebandwindow2", 1.80, 1.93)

mbcSideband_frame = df.plotOn(mbc.frame(40), ROOT.RooFit.CutRange('InvMSideR'))
InvMSideband_frame = df.plotOn(InvM.frame(50), ROOT.RooFit.CutRange('MbcSideR'))
#w=ROOT.RooArgSet(mbc)

#fracSigRange = pdfSig2.createIntegral(w,w,"Region1")
#IncompleteSig_yield = NrecSig.getVal()*fracSigRange.getVal()

#incompleteB = ROOT.RooFormulaVar("events with Bsig=0", "NmisSig + IncompleteSig_yield", ROOT.RooArgList(IncompleteSig_yield,NmisSig))


#fracBkgRange = argus.createIntegral(l,l,"sigwindow")
#bkg_yield = nbkg.getVal()*fracBkgRange.getVal()

#sig_yieldErr = nsig.getError() * fracSigRange.getVal()
#bkg_yieldErr = nbkg.getError() * fracBkgRange.getVal()

#sig_str_yield = "N_{sig} =" +str(int(sig_yield)) + " #pm " + str(int(sig_yieldErr))
#bkg_str_yield = "N_{bkg} =" +str(int(bkg_yield)) + " #pm " + str(int(bkg_yieldErr))


pdf.plotOn(InvM_frame,ROOT.RooFit.Components('pdfSig1'), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('Reco. signal'))
pdf.plotOn(InvM_frame,ROOT.RooFit.Components('pdfSig2'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.Name('Mis-reco. signal'))
pdf.plotOn(InvM_frame,ROOT.RooFit.Components('InvM_Continuum'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kViolet),ROOT.RooFit.Name('Continuum'))
pdf.plotOn(InvM_frame,ROOT.RooFit.Components('pdfGeneric'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kOrange+1),ROOT.RooFit.Name('Generic'))
pdf.plotOn(InvM_frame,ROOT.RooFit.Components('NeutralCrossfeed'),ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kGreen+3),ROOT.RooFit.Name('Neutral-cross.'))

pdf.plotOn(mbc_frame,ROOT.RooFit.Components('pdfSig1'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('Reco. signal'))
pdf.plotOn(mbc_frame,ROOT.RooFit.Components('SigBkg_Novosibirsk'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.Name('Mis-reco. signal'))
pdf.plotOn(mbc_frame,ROOT.RooFit.Components('continuum_pdf'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kViolet),ROOT.RooFit.Name('Continuum'))
pdf.plotOn(mbc_frame,ROOT.RooFit.Components('Generic_Mbc'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2),ROOT.RooFit.LineColor(ROOT.kOrange+1),ROOT.RooFit.Name('Generic'))
pdf.plotOn(mbc_frame,ROOT.RooFit.Components('NeutralCrossfeed'),ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineWidth(2),ROOT.RooFit.LineColor(ROOT.kGreen+3),ROOT.RooFit.Name('Neutral-cross.'))
pdf.plotOn(mbc_frame,ROOT.RooFit.ProjectionRange('Region2'), ROOT.RooFit.LineWidth(3), ROOT.RooFit.LineColor(ROOT.kBlack))#,ROOT.RooFit.LineColor(ROOT.kBlack))
pdf.plotOn(InvM_frame,ROOT.RooFit.ProjectionRange('Region1'), ROOT.RooFit.LineWidth(3),ROOT.RooFit.LineColor(ROOT.kBlack))#,ROOT.RooFit.LineColor(ROOT.kBlack))



c1 = ROOT.TCanvas("c1", "c1",1200,600)
#c2 = ROOT.TCanvas("c2", "c2",600,600)
c1.Divide(2,1)
c1.cd(1)
pad11 = ROOT.TPad("pad11", "The pad 80% of the height",0.0,0.2,1.0,1.0,0)
pad12 = ROOT.TPad("pad12", "The pad 20% of the height",0.0,0.0,1.0,0.2,0)
pad11.SetBottomMargin(0.06)
pad12.SetTopMargin(0.06)
pad12.SetBottomMargin(0.25)

pad11.Draw()
pad12.Draw()


l = ROOT.TLatex()
l.SetNDC()
l.SetTextColor(1)
line1 = ROOT.TLine(5.25, 0, 5.29, 0)
line2 = ROOT.TLine(1.8, 0, 1.93, 0)
line1.SetLineColor(ROOT.kRed)
line2.SetLineColor(ROOT.kRed)




pad12.cd()

MbcResidual = mbc_frame.pullHist()
x1rframe = mbc.frame(ROOT.RooFit.Title("Pull Distribution"))
x1rframe.addPlotable(MbcResidual,"P")
x1rframe.Draw()
line1.SetLineWidth(2)
line1.Draw()
x1rframe.GetYaxis().SetTitleSize(0.12)
x1rframe.GetXaxis().SetTickLength(0.)
x1rframe.GetXaxis().SetLabelSize(0.0)
x1rframe.GetYaxis().SetLabelSize(0.1)
x1rframe.GetXaxis().SetTitleOffset(.45)
x1rframe.GetXaxis().SetTickLength(0.)
x1rframe.GetXaxis().SetLabelSize(0.0)
x1rframe.GetYaxis().CenterTitle()
x1rframe.GetYaxis().SetTitleOffset(0.45)
x1rframe.GetXaxis().SetTitleOffset(.4)
x1rframe.GetXaxis().SetTitleSize(0.17)

pad11.cd()

mbc_frame.Draw()
mbc_frame.SetTitle('')
mbc_frame.GetYaxis().SetTitleOffset(1.45)
mbc_frame.GetXaxis().SetTitleSize(0.09)

leg = ROOT.TLegend(0.1,0.5,0.5,0.7)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextFont(40)
leg.SetTextSize(0.042)
leg.AddEntry(mbc_frame.findObject('Reco. signal'),'reco. signal','l')
leg.AddEntry(mbc_frame.findObject('Mis-reco. signal'),'mis-reco. signal','l')
leg.AddEntry(mbc_frame.findObject('Generic'),'generic background','l')
leg.AddEntry(mbc_frame.findObject('Neutral-cross.'),'neutral-cross. background','l')
leg.AddEntry(mbc_frame.findObject('Continuum'),'continuum background','l')
leg.Draw()

l.DrawLatex(0.2, 0.75, "#it{#Chi^{2}/n.d.f.} =  " + "{:.2f}".format(mbc_frame.chiSquare()))
l.DrawLatex(0.2, 0.8, "Full range")

c1.cd(2)
pad21 = ROOT.TPad("pad21", "The pad 80% of the height",0.0,0.2,1.0,1.0,0)
pad22 = ROOT.TPad("pad22", "The pad 20% of the height",0.0,0.0,1.0,0.2,0)
pad21.SetBottomMargin(0.06)
pad22.SetTopMargin(0.06)
pad22.SetBottomMargin(0.25)
pad21.Draw()
pad22.Draw()


pad22.cd()
InvMResidual = InvM_frame.pullHist()
x2rframe = InvM.frame(ROOT.RooFit.Title("Pull Distribution"))
x2rframe.addPlotable(InvMResidual,"P")
x2rframe.Draw()
line2.SetLineWidth(2)
line2.Draw()
x2rframe.GetXaxis().SetTickLength(0.)
x2rframe.GetXaxis().SetLabelSize(0.0)
x2rframe.GetYaxis().CenterTitle()
x2rframe.GetYaxis().SetTitleOffset(0.45)
x2rframe.GetYaxis().SetTitleSize(0.12)
x2rframe.GetYaxis().SetLabelSize(0.1)
x2rframe.GetXaxis().SetTitleSize(0.17)
x2rframe.GetXaxis().SetTitleOffset(0.4)
pad21.cd()
InvM_frame.Draw()
InvM_frame.SetTitle('')
InvM_frame.GetYaxis().SetTitleOffset(1.45)
InvM_frame.GetXaxis().SetTitleSize(0.09)
l.DrawLatex(0.6, 0.7, "#it{#Chi^{2}/n.d.f.} = " + "{:.2f}".format( InvM_frame.chiSquare()))
l.DrawLatex(0.6, 0.8, "Full range")





c1.Print('stream0_chargedControlD0_Total_2DFit.png')#_sigmaCB1_InvMsigma.png')#free_sigfrac_InvMsigma.png')#free_sigfrac_Mbc_width_totally_free_Argus_slopes_free.png')#fixed_Generic_continuum_crossfeed.png')#_MbcInvMsigmaR_allFree.png')#')#__free_sigfrac_sigma_R1.png')#_MbcInvMsigmaR_allFree.png')#Argus_sum_fixed_ratio.png')#_Argus_fixed_endpoint.png')totally_fixed
c1.Print('stream0_chargedControlD0_Total_2DFit.pdf')#
result.Print()
TotSigErr =  TotSig.getPropagatedError(result)
TotErr =  Tot.getPropagatedError(result)
#IncompleteBerr = incompleteB.getPropagatedError(result)
print("Total  normalization = " +"{:.0f}".format(Tot.getVal())+" +/- "+ "{:.0f}".format(TotErr))
print("Total Signal normalization = " +"{:.0f}".format(TotSig.getVal())+" +/- "+ "{:.0f}".format(TotSigErr))
print("  (includes  correlations) "  )

#print("signal in signal window: "+str(int(sig_yield)))
#print("IncompleteB signal in CB2: "+str(int(IncompleteSig_yield)))

#print("Total incompleteB events = "+"{:.0f}".format(incompleteB.getVal())+" +/- "+ "{:.0f}".format(IncompleteBerr))

print("Mbc fit Chi2/n.d.f. = " + str(mbc_frame.chiSquare()))
print("InvM fit Chi2/n.d.f. = " + str( InvM_frame.chiSquare()))




pdf.plotOn(InvMSignal_frame,ROOT.RooFit.ProjectionRange('MbcSigR'),ROOT.RooFit.Components('pdfSig1'), ROOT.RooFit.LineStyle(ROOT.kDashed),  ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('Reco. signal'))
pdf.plotOn(InvMSignal_frame,ROOT.RooFit.ProjectionRange('MbcSigR'),ROOT.RooFit.Components('pdfSig2'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.Name('Mis-reco. signal'))
pdf.plotOn(InvMSignal_frame,ROOT.RooFit.ProjectionRange('MbcSigR'),ROOT.RooFit.Components('InvM_Continuum'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kViolet),ROOT.RooFit.Name('Continuum'))
pdf.plotOn(InvMSignal_frame,ROOT.RooFit.ProjectionRange('MbcSigR'),ROOT.RooFit.Components('pdfGeneric'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kOrange+1),ROOT.RooFit.Name('Generic'))
pdf.plotOn(InvMSignal_frame,ROOT.RooFit.ProjectionRange('MbcSigR'),ROOT.RooFit.Components('NeutralCrossfeed'),ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kGreen+3),ROOT.RooFit.Name('Neutral-cross.'))

pdf.plotOn(mbcSignal_frame,ROOT.RooFit.ProjectionRange('InvMSigR'),ROOT.RooFit.Components('pdfSig1'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('Reco. signal'))
pdf.plotOn(mbcSignal_frame,ROOT.RooFit.ProjectionRange('InvMSigR'),ROOT.RooFit.Components('SigBkg_Novosibirsk'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.Name('Mis-reco. signal'))
pdf.plotOn(mbcSignal_frame,ROOT.RooFit.ProjectionRange('InvMSigR'),ROOT.RooFit.Components('continuum_pdf'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kViolet),ROOT.RooFit.Name('Continuum'))
pdf.plotOn(mbcSignal_frame,ROOT.RooFit.ProjectionRange('InvMSigR'),ROOT.RooFit.Components('Generic_Mbc'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2),ROOT.RooFit.LineColor(ROOT.kOrange+1),ROOT.RooFit.Name('Generic'))
pdf.plotOn(mbcSignal_frame,ROOT.RooFit.ProjectionRange('InvMSigR'),ROOT.RooFit.Components('NeutralCrossfeed'),ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineWidth(2),ROOT.RooFit.LineColor(ROOT.kGreen+3),ROOT.RooFit.Name('Neutral-cross.'))
pdf.plotOn(mbcSignal_frame,ROOT.RooFit.ProjectionRange('InvMSigR'), ROOT.RooFit.LineWidth(3), ROOT.RooFit.LineColor(ROOT.kBlack))#,ROOT.RooFit.LineColor(ROOT.kBlack))
pdf.plotOn(InvMSignal_frame,ROOT.RooFit.ProjectionRange('MbcSigR'), ROOT.RooFit.LineWidth(3),ROOT.RooFit.LineColor(ROOT.kBlack))
#pdf.plotOn(InvMSignal_frame,ROOT.RooFit.ProjectionRange('MbcSigR'), ROOT.RooFit.CutRange('InvMSigR'), ROOT.RooFit.FillStyle(3004), ROOT.RooFit.FillColor(-4))

c2 = ROOT.TCanvas("c2", "c2",1200,600)
c2.Divide(2,1)
c2.cd(1)
pad33 = ROOT.TPad("pad33", "The pad 80% of the height",0.0,0.2,1.0,1.0,0)
pad13 = ROOT.TPad("pad13", "The pad 20% of the height",0.0,0.0,1.0,0.2,0)
pad33.SetBottomMargin(0.06)
pad13.SetTopMargin(0.06)
pad13.SetBottomMargin(0.25)

pad33.Draw()
pad13.Draw()


l = ROOT.TLatex()
l.SetNDC()
l.SetTextColor(1)
line1 = ROOT.TLine(5.25, 0, 5.29, 0)
line2 = ROOT.TLine(1.8, 0, 1.93, 0)
line1.SetLineColor(ROOT.kRed)
line2.SetLineColor(ROOT.kRed)


pad13.cd()

MbcResidual = mbcSignal_frame.pullHist()
x1rframe = mbc.frame(ROOT.RooFit.Title("Pull Distribution"))
x1rframe.addPlotable(MbcResidual,"P")
x1rframe.Draw()
line1.SetLineWidth(2)
line1.Draw()
#x1rframe.GetYaxis().SetTitle('Pull      ')
#x1rframe.GetYaxis().SetTitleSize(0.13)
x1rframe.GetYaxis().SetTitleSize(0.1)
x1rframe.GetXaxis().SetTickLength(0.)
x1rframe.GetXaxis().SetLabelSize(0.0)
x1rframe.GetYaxis().SetLabelSize(0.09)
x1rframe.GetXaxis().SetTitleOffset(.45)
x1rframe.GetXaxis().SetTitleSize(0.2)


pad33.cd()

mbcSignal_frame.Draw()
mbcSignal_frame.SetTitle('')
mbcSignal_frame.GetYaxis().SetTitleOffset(1.45)
mbcSignal_frame.GetXaxis().SetTitleSize(0.09)

MbcSigMin = ROOT.TLine(5.27, 0, 5.27, 5000)#pad33.GetUymax())
MbcSigMin.SetLineStyle(10)
MbcSigMin.SetLineWidth(3)
#MbcSigMin.SetLineColor(ROOT.kMagenta)
MbcSigMin.Draw()

MbcSigMax = ROOT.TLine(5.29, 0, 5.29, 5000)#pad33.GetUymax())
MbcSigMax.SetLineStyle(10)
MbcSigMax.SetLineWidth(3)
#MbcSigMax.SetLineColor(ROOT.kMagenta)
MbcSigMax.Draw()


leg = ROOT.TLegend(0.12,0.35,0.5,0.6)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextFont(40)
leg.SetTextSize(0.045)
leg.AddEntry(mbcSignal_frame.findObject('Reco. signal'),'reco. signal','l')
leg.AddEntry(mbcSignal_frame.findObject('Mis-reco. signal'),'mis-reco. signal','l')
leg.AddEntry(mbcSignal_frame.findObject('Generic'),'generic background','l')
leg.AddEntry(mbcSignal_frame.findObject('Neutral-cross.'),'neutral-cross. background','l')
leg.AddEntry(mbcSignal_frame.findObject('Continuum'),'continuum background','l')
leg.Draw()

l.DrawLatex(0.2, 0.7, "#it{#Chi^{2}/n.d.f.} =  " + "{:.2f}".format(mbcSignal_frame.chiSquare()))
l.DrawLatex(0.2, 0.8, "Signal window")

c2.cd(2)
pad31 = ROOT.TPad("pad31", "The pad 80% of the height",0.0,0.2,1.0,1.0,0)
pad33 = ROOT.TPad("pad33", "The pad 20% of the height",0.0,0.0,1.0,0.2,0)
pad31.SetBottomMargin(0.06)
pad33.SetTopMargin(0.06)
pad33.SetBottomMargin(0.25)
pad31.Draw()
pad33.Draw()


pad33.cd()
InvMResidual = InvMSignal_frame.pullHist()
x2rframe = InvM.frame(ROOT.RooFit.Title("Pull Distribution"))
x2rframe.addPlotable(InvMResidual,"P")
x2rframe.Draw()
line2.SetLineWidth(2)
line2.Draw()
x2rframe.GetXaxis().SetTickLength(0.)
x2rframe.GetXaxis().SetLabelSize(0.0)
x2rframe.GetYaxis().CenterTitle()
x2rframe.GetYaxis().SetTitleOffset(0.45)
x2rframe.GetYaxis().SetTitleSize(0.12)
x2rframe.GetYaxis().SetLabelSize(0.1)
x2rframe.GetXaxis().SetTitleSize(0.17)
x2rframe.GetXaxis().SetTitleOffset(0.4)

pad31.cd()
InvMSignal_frame.Draw()
InvMSignal_frame.SetTitle('')
InvMSignal_frame.GetYaxis().SetTitleOffset(1.45)
InvMSignal_frame.GetXaxis().SetTitleSize(0.09)

InvMSigMin = ROOT.TLine(1.85, 0, 1.85, 6500)#pad33.GetUymax())
InvMSigMin.SetLineStyle(10)
InvMSigMin.SetLineWidth(3)
InvMSigMin.SetLineColor(ROOT.kMagenta)
InvMSigMin.Draw()

InvMSigMax = ROOT.TLine(1.88, 0, 1.88, 6500)#pad33.GetUymax())
InvMSigMax.SetLineStyle(10)
InvMSigMax.SetLineWidth(3)
InvMSigMax.SetLineColor(ROOT.kMagenta)
InvMSigMax.Draw()

l.DrawLatex(0.16, 0.7, "#it{#Chi^{2}/n.d.f.} = " + "{:.2f}".format( InvMSignal_frame.chiSquare()))
l.DrawLatex(0.16, 0.8, "Signal window")





c2.Print('stream0Signal_window_chargedControlD0_Total_2DFit.png')#_sigmaCB1_InvMsigma.png')#free_sigfrac_InvMsigma.png')#free_sigfrac_Mbc_width_totally_free_Argus_slopes_free.png')#fixed_Generic_continuum_crossfeed.png')#_MbcInvMsigmaR_allFree.png')#')#__free_sigfrac_sigma_R1.png')#_MbcInvMsigmaR_allFree.png')#Argus_sum_fixed_ratio.png')#_Argus_fixed_endpoint.png')totally_fixed
c2.Print('stream0Signal_window_chargedControlD0_Total_2DFit.pdf')


pdf.plotOn(InvMSideband_frame,ROOT.RooFit.Components('pdfSig1'), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('Reco. signal'))
pdf.plotOn(InvMSideband_frame,ROOT.RooFit.Components('pdfSig2'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.Name('Mis-reco. signal'))
pdf.plotOn(InvMSideband_frame,ROOT.RooFit.Components('InvM_Continuum'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kViolet),ROOT.RooFit.Name('Continuum'))
pdf.plotOn(InvMSideband_frame,ROOT.RooFit.Components('pdfGeneric'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kOrange+1),ROOT.RooFit.Name('Generic'))
pdf.plotOn(InvMSideband_frame,ROOT.RooFit.Components('NeutralCrossfeed'),ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kGreen+3),ROOT.RooFit.Name('Neutral-cross.'))

pdf.plotOn(mbcSideband_frame,ROOT.RooFit.ProjectionRange('InvM_sidebandwindow1'),ROOT.RooFit.Components('pdfSig1'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('Reco. signal'))
pdf.plotOn(mbcSideband_frame,ROOT.RooFit.ProjectionRange('InvM_sidebandwindow1'),ROOT.RooFit.Components('pdfSig2'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.Name('Mis-reco. signal'))
pdf.plotOn(mbcSideband_frame,ROOT.RooFit.ProjectionRange('InvM_sidebandwindow1'),ROOT.RooFit.Components('continuum_pdf'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kViolet),ROOT.RooFit.Name('Continuum'))
pdf.plotOn(mbcSideband_frame,ROOT.RooFit.ProjectionRange('InvM_sidebandwindow1'),ROOT.RooFit.Components('pdfGeneric'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2),ROOT.RooFit.LineColor(ROOT.kOrange+1),ROOT.RooFit.Name('Generic'))
pdf.plotOn(mbcSideband_frame,ROOT.RooFit.ProjectionRange('InvM_sidebandwindow1'),ROOT.RooFit.Components('NeutralCrossfeed'),ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineWidth(2),ROOT.RooFit.LineColor(ROOT.kGreen+3),ROOT.RooFit.Name('Neutral-cross.'))
pdf.plotOn(mbcSideband_frame, ROOT.RooFit.LineWidth(3), ROOT.RooFit.LineColor(ROOT.kBlack))#,ROOT.RooFit.LineColor(ROOT.kBlack))
pdf.plotOn(InvMSideband_frame,ROOT.RooFit.ProjectionRange('InvM_sidebandwindow1'), ROOT.RooFit.LineWidth(3),ROOT.RooFit.LineColor(ROOT.kBlack))
#pdf.plotOn(InvMSignal_frame,ROOT.RooFit.ProjectionRange('MbcSigR'), ROOT.RooFit.CutRange('InvMSigR'), ROOT.RooFit.FillStyle(3004), ROOT.RooFit.FillColor(-4))

c3 = ROOT.TCanvas("c3", "c3",1200,600)
c3.Divide(2,1)
c3.cd(1)
pad32 = ROOT.TPad("pad33", "The pad 80% of the height",0.0,0.2,1.0,1.0,0)
pad13 = ROOT.TPad("pad13", "The pad 20% of the height",0.0,0.0,1.0,0.2,0)
pad32.SetBottomMargin(0.06)
pad13.SetTopMargin(0.06)
pad13.SetBottomMargin(0.25)

pad32.Draw()
pad13.Draw()


l = ROOT.TLatex()
l.SetNDC()
l.SetTextColor(1)
line1 = ROOT.TLine(5.25, 0, 5.29, 0)
line2 = ROOT.TLine(1.8, 0, 1.93, 0)
line1.SetLineColor(ROOT.kRed)
line2.SetLineColor(ROOT.kRed)


pad13.cd()

MbcResidual = mbcSideband_frame.pullHist()
x1rframe = mbc.frame(ROOT.RooFit.Title("Pull Distribution"))
x1rframe.addPlotable(MbcResidual,"P")
x1rframe.Draw()
line1.SetLineWidth(2)
line1.Draw()
#x1rframe.GetYaxis().SetTitle('Pull      ')
#x1rframe.GetYaxis().SetTitleSize(0.13)
x1rframe.GetYaxis().SetTitleSize(0.1)
x1rframe.GetXaxis().SetTickLength(0.)
x1rframe.GetXaxis().SetLabelSize(0.0)
x1rframe.GetYaxis().SetLabelSize(0.09)
x1rframe.GetXaxis().SetTitleOffset(.45)
x1rframe.GetXaxis().SetTitleSize(0.2)


pad32.cd()

mbcSideband_frame.Draw()
mbcSideband_frame.GetYaxis().SetTitleOffset(1.45)
mbcSideband_frame.GetXaxis().SetTitleSize(0.09)



l.DrawLatex(0.25, 0.7, "#it{#Chi^{2}/n.d.f.} =  " + "{:.2f}".format(mbcSideband_frame.chiSquare()))
l.DrawLatex(0.3, 0.8, "Sideband ")

c3.cd(2)
pad31 = ROOT.TPad("pad31", "The pad 80% of the height",0.0,0.2,1.0,1.0,0)
pad33 = ROOT.TPad("pad33", "The pad 20% of the height",0.0,0.0,1.0,0.2,0)
pad31.SetBottomMargin(0.06)
pad33.SetTopMargin(0.06)
pad33.SetBottomMargin(0.25)
pad31.Draw()
pad33.Draw()


pad33.cd()
InvMResidual = InvM_frame.pullHist()
x2rframe = InvM.frame(ROOT.RooFit.Title("Pull Distribution"))
x2rframe.addPlotable(InvMResidual,"P")
x2rframe.Draw()
line2.SetLineWidth(2)
line2.Draw()
x2rframe.GetXaxis().SetTickLength(0.)
x2rframe.GetXaxis().SetLabelSize(0.0)
x2rframe.GetYaxis().SetLabelSize(0.09)
x2rframe.GetXaxis().SetTitleOffset(.45)
x2rframe.GetXaxis().SetTitleSize(0.2)

pad31.cd()
InvM_frame.Draw()
InvM_frame.SetTitle('')
InvM_frame.GetYaxis().SetTitleOffset(1.45)
InvM_frame.GetXaxis().SetTitleSize(0.09)

InvMSigMin = ROOT.TLine(1.8, 0, 1.8, 8000)#pad33.GetUymax())
InvMSigMin.SetLineStyle(10)
InvMSigMin.SetLineWidth(3)
InvMSigMin.SetLineColor(ROOT.kRed)
InvMSigMin.Draw()

InvMSigMax = ROOT.TLine(1.84, 0, 1.84, 8000)#pad33.GetUymax())
InvMSigMax.SetLineStyle(10)
InvMSigMax.SetLineWidth(3)
InvMSigMax.SetLineColor(ROOT.kRed)
InvMSigMax.Draw()



l.DrawLatex(0.6, 0.7, "#it{#Chi^{2}/n.d.f.} = " + "{:.2f}".format( InvM_frame.chiSquare()))
l.DrawLatex(0.15, 0.8, "Sideband ")





c3.Print('InvM_sideband_stream0_chargedControlD0_Total_2DFit.png')#_sigmaCB1_InvMsigma.png')#free_sigfrac_InvMsigma.png')#free_sigfrac_Mbc_width_totally_free_Argus_slopes_free.png')#fixed_Generic_continuum_crossfeed.png')#_MbcInvMsigmaR_allFree.png')#')#__free_sigfrac_sigma_R1.png')#_MbcInvMsigmaR_allFree.png')#Argus_sum_fixed_ratio.png')#_Argus_fixed_endpoint.png')totally_fixed
c3.Print('InvM_sideband_stream0_chargedControlD0_Total_2DFit.pdf')


mbcSideband_frame2 = df.plotOn(mbc.frame(40))
InvMSideband_frame2 = df.plotOn(InvM.frame(50), ROOT.RooFit.CutRange('Mbc_sidebandwindow2'))


pdf.plotOn(InvMSideband_frame2, ROOT.RooFit.ProjectionRange('Mbc_sidebandwindow2'),ROOT.RooFit.Components('pdfSig1'), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('Reco. signal'))
pdf.plotOn(InvMSideband_frame2, ROOT.RooFit.ProjectionRange('Mbc_sidebandwindow2'),ROOT.RooFit.Components('pdfSig2'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.Name('Mis-reco. signal'))
pdf.plotOn(InvMSideband_frame2, ROOT.RooFit.ProjectionRange('Mbc_sidebandwindow2'),ROOT.RooFit.Components('InvM_Continuum'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kViolet),ROOT.RooFit.Name('Continuum'))
pdf.plotOn(InvMSideband_frame2, ROOT.RooFit.ProjectionRange('Mbc_sidebandwindow2'),ROOT.RooFit.Components('pdfGeneric'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kOrange+1),ROOT.RooFit.Name('Generic'))
pdf.plotOn(InvMSideband_frame2, ROOT.RooFit.ProjectionRange('Mbc_sidebandwindow2'),ROOT.RooFit.Components('NeutralCrossfeed'),ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kGreen+3),ROOT.RooFit.Name('Neutral-cross.'))

pdf.plotOn(mbcSideband_frame2,ROOT.RooFit.Components('pdfSig1'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('Reco. signal'))
pdf.plotOn(mbcSideband_frame2,ROOT.RooFit.Components('pdfSig2'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.Name('Mis-reco. signal'))
pdf.plotOn(mbcSideband_frame2,ROOT.RooFit.Components('continuum_pdf'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2), ROOT.RooFit.LineColor(ROOT.kViolet),ROOT.RooFit.Name('Continuum'))
pdf.plotOn(mbcSideband_frame2,ROOT.RooFit.Components('pdfGeneric'),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineWidth(2),ROOT.RooFit.LineColor(ROOT.kOrange+1),ROOT.RooFit.Name('Generic'))
pdf.plotOn(mbcSideband_frame2,ROOT.RooFit.Components('NeutralCrossfeed'),ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineWidth(2),ROOT.RooFit.LineColor(ROOT.kGreen+3),ROOT.RooFit.Name('Neutral-cross.'))
pdf.plotOn(mbcSideband_frame2, ROOT.RooFit.LineWidth(3), ROOT.RooFit.LineColor(ROOT.kBlack))#,ROOT.RooFit.LineColor(ROOT.kBlack))
pdf.plotOn(InvMSideband_frame2, ROOT.RooFit.ProjectionRange('Mbc_sidebandwindow2'), ROOT.RooFit.LineWidth(3),ROOT.RooFit.LineColor(ROOT.kBlack))
#pdf.plotOn(InvMSignal_frame,ROOT.RooFit.ProjectionRange('MbcSigR'), ROOT.RooFit.CutRange('InvMSigR'), ROOT.RooFit.FillStyle(3004), ROOT.RooFit.FillColor(-4))

c4 = ROOT.TCanvas("c4", "c4",1200,600)
c4.Divide(2,1)
c4.cd(1)
pad30 = ROOT.TPad("pad33", "The pad 80% of the height",0.0,0.2,1.0,1.0,0)
pad13 = ROOT.TPad("pad13", "The pad 20% of the height",0.0,0.0,1.0,0.2,0)
pad30.SetBottomMargin(0.06)
pad13.SetTopMargin(0.06)
pad13.SetBottomMargin(0.25)

pad30.Draw()
pad13.Draw()


l = ROOT.TLatex()
l.SetNDC()
l.SetTextColor(1)
line1 = ROOT.TLine(5.25, 0, 5.29, 0)
line2 = ROOT.TLine(1.8, 0, 1.93, 0)
line1.SetLineColor(ROOT.kRed)
line2.SetLineColor(ROOT.kRed)


pad13.cd()

MbcResidual = mbc_frame.pullHist()
x1rframe = mbc.frame(ROOT.RooFit.Title("Pull Distribution"))
x1rframe.addPlotable(MbcResidual,"P")
x1rframe.Draw()
line1.SetLineWidth(2)
line1.Draw()
#x1rframe.GetYaxis().SetTitle('Pull      ')
#x1rframe.GetYaxis().SetTitleSize(0.12)
x1rframe.GetYaxis().SetTitleSize(0.1)
x1rframe.GetXaxis().SetTickLength(0.)
x1rframe.GetXaxis().SetLabelSize(0.0)
x1rframe.GetYaxis().SetLabelSize(0.09)
x1rframe.GetXaxis().SetTitleOffset(.45)
x1rframe.GetXaxis().SetTitleSize(0.2)



pad30.cd()

mbc_frame.Draw()
mbc_frame.SetTitle('')
mbc_frame.GetYaxis().SetTitleOffset(1.45)
mbc_frame.GetXaxis().SetTitleSize(0.09)

MbcSideMin = ROOT.TLine(5.25, 0, 5.25, 5000)#pad33.GetUymax())
MbcSideMin.SetLineStyle(10)
MbcSideMin.SetLineWidth(3)
MbcSideMin.SetLineColor(ROOT.kRed)
MbcSideMin.Draw()

MbcSideMax = ROOT.TLine(5.265, 0, 5.265, 5000)#pad33.GetUymax())
MbcSideMax.SetLineStyle(10)
MbcSideMax.SetLineWidth(3)
MbcSideMax.SetLineColor(ROOT.kRed)
MbcSideMax.Draw()

l.DrawLatex(0.2, 0.7, "#it{#Chi^{2}/n.d.f.} =  " + "{:.2f}".format(mbc_frame.chiSquare()))
l.DrawLatex(0.3, 0.8, "Sideband ")

c4.cd(2)
pad31 = ROOT.TPad("pad31", "The pad 80% of the height",0.0,0.2,1.0,1.0,0)
pad33 = ROOT.TPad("pad33", "The pad 20% of the height",0.0,0.0,1.0,0.2,0)
pad31.SetBottomMargin(0.06)
pad33.SetTopMargin(0.06)
pad33.SetBottomMargin(0.25)
pad31.Draw()
pad33.Draw()


pad33.cd()
InvMResidual = InvMSideband_frame2.pullHist()
x2rframe = InvM.frame(ROOT.RooFit.Title("Pull Distribution"))
x2rframe.addPlotable(InvMResidual,"P")
x2rframe.Draw()
line2.SetLineWidth(2)
line2.Draw()
x2rframe.GetXaxis().SetTickLength(0.)
x2rframe.GetXaxis().SetLabelSize(0.0)
x2rframe.GetYaxis().SetLabelSize(0.09)
x2rframe.GetXaxis().SetTitleOffset(.45)
x2rframe.GetXaxis().SetTitleSize(0.2)

pad31.cd()
InvMSideband_frame2.Draw()
InvMSideband_frame2.SetTitle('')
InvMSideband_frame2.GetYaxis().SetTitleOffset(1.45)
InvMSideband_frame2.GetXaxis().SetTitleSize(0.09)




l.DrawLatex(0.15, 0.7, "#it{#Chi^{2}/n.d.f.} = " + "{:.2f}".format( InvMSideband_frame2.chiSquare()))
l.DrawLatex(0.15, 0.8, "Sideband ")





c4.Print('Mbc_sideband_stream0_chargedControlD0_Total_2DFit.png')#_sigmaCB1_InvMsigma.png')#free_sigfrac_InvMsigma.png')#free_sigfrac_Mbc_width_totally_free_Argus_slopes_free.png')#fixed_Generic_continuum_crossfeed.png')#_MbcInvMsigmaR_allFree.png')#')#__free_sigfrac_sigma_R1.png')#_MbcInvMsigmaR_allFree.png')#Argus_sum_fixed_ratio.png')#_Argus_fixed_endpoint.png')totally_fixed
c4.Print('Mbc_sideband_stream0_chargedControlD0_Total_2DFit.pdf')


