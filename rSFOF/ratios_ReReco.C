//
// Macro to get the R_sf/of ratios and corresponding uncertainties
//
// Run as: root -l -q -b ratios.C
//

static const int precision = 4;

class Observable {
  // Yet another value - error class
public:
  Observable(float& value = 0., float& error = 0., float& syst = 0.):v(value),e(error),s(syst) {} 
  // members
  float v,e,s;
  // methods

  const float e2(void) const { return e*e; }
  const float s2(void) const { return s*s; }

  const float t(void) const { return sqrt(e2()+s2()); }
  const float t2(void) const { return e2()+s2(); }

  void roundUp( const int digits ) { 
    v = TMath::Nint(v*TMath::Power(10.,digits))/TMath::Power(10.,digits);
    e = TMath::Nint(e*TMath::Power(10.,digits))/TMath::Power(10.,digits);
    s = TMath::Nint(s*TMath::Power(10.,digits))/TMath::Power(10.,digits);
  };

  friend ostream &operator <<(ostream &, const string &);
  
};

ostream &operator<<(ostream &stream, const Observable &o)
{
  if ( o.s < 1e-12 ) {
    return(stream << o.v << "+-" << o.t() << " [" << o.t()/o.v*100. << "%]");
  }

  return(stream << o.v << "+-" << o.e << "+-" << o.s << " (total unc. " << o.t() << " [" << o.t()/o.v*100. << "%])");    
    

}


float getRatioAndError(int a, int b, float& r, float& err) { 
  r   = a/static_cast<float>(b); 
  err = r*sqrt(1/float(a)+1/float(b));
}

float getRmueAndError(int a, int b, float& r, float& err) { 
  r   = sqrt(a/static_cast<float>(b)); 
  err = 0.5*r*sqrt(1/float(a)+1/float(b));
}

float getRTandErrorCR(int ee, int mm, int em, float& RT, float& err) { 
  RT   = 2.0*sqrt(ee*mm)/static_cast<float>(em); 
  err = RT*sqrt(1/float(4.0*ee)+1/float(4.0*mm)+1/float(em));
}

void getEfficiency(int num, int den, Observable& eff, float& relsys ) { 
  eff.v = num/static_cast<float>(den);
  float up = TEfficiency::ClopperPearson(den,num,0.68,true) - eff.v;
  float down = -TEfficiency::ClopperPearson(den,num,0.68,false) + eff.v;
  eff.e = TMath::Max(up,down);
  eff.s = relsys*eff.v;
}

float getRelRTerr(float EE, float MM, float EM, float errEE, float errMM, float errEM) { 
  return sqrt((errEE*errEE)/(4.0*EE*EE*MM*MM)+(errMM*errMM)/(4.0*EE*EE*MM*MM) + (errEM*errEM)/(EM*EM)); 
}

float getRTandError(Observable eeEff, Observable mmEff, Observable emEff, Observable& RT) { 
  RT.v = sqrt(eeEff.v*mmEff.v)/emEff.v;
  RT.e = RT.v*getRelRTerr(eeEff.v,mmEff.v,emEff.v,eeEff.e,mmEff.e,emEff.e);
  RT.s = RT.v*getRelRTerr(eeEff.v,mmEff.v,emEff.v,eeEff.s,mmEff.s,emEff.s);
}

float getRsfofFromRmue(Observable rmue, Observable& rsfof ) { 
  rsfof.v =  0.5*(rmue.v+1.0/rmue.v);
  float f = 0.5*( 1.0 - 1.0/(rmue.v*rmue.v) );
  rsfof.e = f*rmue.e;
  rsfof.s = f*rmue.s;
}




//_________________________________________________________________________________
int ratios_ReReco(void) {

  float lumifactor = 9.2/9.2;

  //---------------------------------------------------------------------
  // 1. R(SF/OF) from R_mue and trigger eff.

  //-- R(SF/OF) from R_mue
  Observable rmue_c; //1.101,0.0); rmue_c.s = rmue_c.v*0.10; // Neglect stat. unc. <--- CHECK
  Observable rmue_f; //1.209,0.0); rmue_f.s = rmue_f.v*0.20; // Neglect stat. unc. <--- CHECK
  getRmueAndError(99144*lumifactor,83761*lumifactor,rmue_c.v,rmue_c.e);
  getRmueAndError(62778*lumifactor,44829*lumifactor,rmue_f.v,rmue_f.e);
//  getRmueAndError(45476,38364,rmue_c.v,rmue_c.e);
//  getRmueAndError(28765,20429,rmue_f.v,rmue_f.e);
  rmue_c.s = rmue_c.v*0.10;
  rmue_f.s = rmue_f.v*0.20;
  
  Observable rsfof_rmue_c, rsfof_rmue_f;
  getRsfofFromRmue(rmue_c,rsfof_rmue_c);
  getRsfofFromRmue(rmue_f,rsfof_rmue_f);

  //-- R(SF/OF) for trigger eff.
  int kEE_c = 3592*lumifactor, nEE_c = 3692*lumifactor, kMM_c = 1375*lumifactor, nMM_c = 1420*lumifactor, kEM_c = 493*lumifactor, nEM_c = 521*lumifactor;
  int kEE_f =  954*lumifactor, nEE_f =  980*lumifactor, kMM_f =  547*lumifactor, nMM_f =  566*lumifactor, kEM_f = 102*lumifactor, nEM_f = 114*lumifactor;

  float srtrig_c = 0.05; // Relative systematic uncertainty on trigger efficiencies
  float srtrig_f = 0.05;
  
  // Trigger efficiencies
  Observable trigEE_c, trigMM_c, trigEM_c;
  getEfficiency(kEE_c,nEE_c,trigEE_c,srtrig_c);
  getEfficiency(kMM_c,nMM_c,trigMM_c,srtrig_c);
  getEfficiency(kEM_c,nEM_c,trigEM_c,srtrig_c);
  
  Observable trigEE_f, trigMM_f, trigEM_f;
  getEfficiency(kEE_f,nEE_f,trigEE_f,srtrig_f);
  getEfficiency(kMM_f,nMM_f,trigMM_f,srtrig_f);
  getEfficiency(kEM_f,nEM_f,trigEM_f,srtrig_f);
  
  // Resulting RT
  Observable RT_c, RT_f;
  getRTandError(trigEE_c,trigMM_c,trigEM_c,RT_c);
  getRTandError(trigEE_f,trigMM_f,trigEM_f,RT_f);
  
  //-- Folding them together
  Observable Rsfof_c(rsfof_rmue_c.v*RT_c.v);
  Rsfof_c.e  = Rsfof_c.v*sqrt(rsfof_rmue_c.e*rsfof_rmue_c.e/(rsfof_rmue_c.v*rsfof_rmue_c.v)+RT_c.e*RT_c.e/(RT_c.v*RT_c.v));
  Rsfof_c.s  = Rsfof_c.v*sqrt(rsfof_rmue_c.s*rsfof_rmue_c.s/(rsfof_rmue_c.v*rsfof_rmue_c.v)+RT_c.s*RT_c.s/(RT_c.v*RT_c.v));
  Observable Rsfof_f(rsfof_rmue_f.v*RT_f.v);
  Rsfof_f.e  = Rsfof_f.v*sqrt(rsfof_rmue_f.e*rsfof_rmue_f.e/(rsfof_rmue_f.v*rsfof_rmue_f.v)+RT_f.e*RT_f.e/(RT_f.v*RT_f.v));
  Rsfof_f.s  = Rsfof_f.v*sqrt(rsfof_rmue_f.s*rsfof_rmue_f.s/(rsfof_rmue_f.v*rsfof_rmue_f.v)+RT_f.s*RT_f.s/(RT_f.v*RT_f.v));
//  Rsfof_f.e  = sqrt(rsfof_rmue_f.e*rsfof_rmue_f.e+RT_f.e*RT_f.e); 
//  Rsfof_f.s  = sqrt(rsfof_rmue_f.s*rsfof_rmue_f.s+RT_f.s*RT_f.s);
  
  Observable  ReeOF_c(0.5/rmue_c.v*RT_c.v);
  ReeOF_c.e = ReeOF_c.v*sqrt(rmue_c.e*rmue_c.e/(rmue_c.v*rmue_c.v)+RT_c.e*RT_c.e/(RT_c.v*RT_c.v));
  ReeOF_c.s = ReeOF_c.v*sqrt(rmue_c.s*rmue_c.s/(rmue_c.v*rmue_c.v)+RT_c.s*RT_c.s/(RT_c.v*RT_c.v));
  Observable  ReeOF_f(0.5/rmue_f.v*RT_f.v);
  ReeOF_f.e = ReeOF_f.v*sqrt(rmue_f.e*rmue_f.e/(rmue_f.v*rmue_f.v)+RT_f.e*RT_f.e/(RT_f.v*RT_f.v));
  ReeOF_f.s = ReeOF_f.v*sqrt(rmue_f.s*rmue_f.s/(rmue_f.v*rmue_f.v)+RT_f.s*RT_f.s/(RT_f.v*RT_f.v));
  
  Observable  RmmOF_c(0.5*rmue_c.v*RT_c.v);
  RmmOF_c.e = RmmOF_c.v*sqrt(rmue_c.e*rmue_c.e/(rmue_c.v*rmue_c.v)+RT_c.e*RT_c.e/(RT_c.v*RT_c.v));
  RmmOF_c.s = RmmOF_c.v*sqrt(rmue_c.s*rmue_c.s/(rmue_c.v*rmue_c.v)+RT_c.s*RT_c.s/(RT_c.v*RT_c.v));
  Observable  RmmOF_f(0.5*rmue_f.v*RT_f.v);
  RmmOF_f.e = RmmOF_f.v*sqrt(rmue_f.e*rmue_f.e/(rmue_f.v*rmue_f.v)+RT_f.e*RT_f.e/(RT_f.v*RT_f.v));
  RmmOF_f.s = RmmOF_f.v*sqrt(rmue_f.s*rmue_f.s/(rmue_f.v*rmue_f.v)+RT_f.s*RT_f.s/(RT_f.v*RT_f.v));
  
  
  std::cout << "-----------------------------------------" << std::endl;
  std::cout << "--        SUMMARY R_MUE METHOD         --" << std::endl;
  std::cout << setprecision(5) << std::fixed;
  std::cout << "rmue central = " << rmue_c << std::endl;
  std::cout << "rmue forward = " << rmue_f << std::endl;
  std::cout << std::endl;
  std::cout << "trigEE central = " << trigEE_c << std::endl;
  std::cout << "trigMM central = " << trigMM_c << std::endl;
  std::cout << "trigEM central = " << trigEM_c << std::endl;
  std::cout << "trigEE forward = " << trigEE_f << std::endl;
  std::cout << "trigMM forward = " << trigMM_f << std::endl;
  std::cout << "trigEM forward = " << trigEM_f << std::endl;
  std::cout << std::endl;
  std::cout << "R_T central = " << RT_c << std::endl;
  std::cout << "R_T forward = " << RT_f << std::endl;
  std::cout << std::endl;
  std::cout << setprecision(precision) << std::fixed;
  std::cout << "Rsfof(rmue) central = " << Rsfof_c << std::endl;
  std::cout << "Reeof(rmue) central = " << ReeOF_c << std::endl;
  std::cout << "Rmmof(rmue) central = " << RmmOF_c << std::endl;
  std::cout << std::endl;
  std::cout << "Rsfof(rmue) forward = " << Rsfof_f << std::endl;
  std::cout << "Reeof(rmue) forward = " << ReeOF_f << std::endl;
  std::cout << "Rmmof(rmue) forward = " << RmmOF_f << std::endl;

  //---------------------------------------------------------------------
  // 2. R(SF/OF) from the CR
  Observable RSFcr_c, Reecr_c, Rmmcr_c, rmueCR_c, RTcr_c;
  Observable RSFcr_f, Reecr_f, Rmmcr_f, rmueCR_f, RTcr_f;
  
  int nEM = 1458*lumifactor, nEE = 669*lumifactor, nMM = 806*lumifactor;
  getRatioAndError(nEE+nMM,nEM,RSFcr_c.v,RSFcr_c.e);
  RSFcr_c.s = RSFcr_c.v*0.01; // Syst. unc. from MC closure
  getRatioAndError(nEE,nEM,Reecr_c.v,Reecr_c.e);
  Reecr_c.s = Reecr_c.v*0.02; // Syst. unc. from MC closure
  getRatioAndError(nMM,nEM,Rmmcr_c.v,Rmmcr_c.e);
  Rmmcr_c.s = Rmmcr_c.v*0.02; // Syst. unc. from MC closure
  
  getRmueAndError(nMM,nEE,rmueCR_c.v,rmueCR_c.e);
  getRTandErrorCR(nEE,nMM,nEM,RTcr_c.v,RTcr_c.e);

  nEM = 547*lumifactor, nEE = 240*lumifactor, nMM = 307*lumifactor;
  getRatioAndError(nEE+nMM,nEM,RSFcr_f.v,RSFcr_f.e);
  RSFcr_f.s = RSFcr_f.v*0.02; // Syst. unc. from MC closure
  getRatioAndError(nEE,nEM,Reecr_f.v,Reecr_f.e);
  Reecr_f.s = Reecr_f.v*0.04; // Syst. unc. from MC closure
  getRatioAndError(nMM,nEM,Rmmcr_f.v,Rmmcr_f.e);
  Rmmcr_f.s = Rmmcr_f.v*0.04; // Syst. unc. from MC closure

  getRmueAndError(nMM,nEE,rmueCR_f.v,rmueCR_f.e);
  getRTandErrorCR(nEE,nMM,nEM,RTcr_f.v,RTcr_f.e);

  
  std::cout << "-----------------------------------------" << std::endl;
  std::cout << "--        SUMMARY CONTROL REGION       --" << std::endl;
  std::cout << setprecision(3) << std::fixed;
  std::cout << "rmue central = " << rmueCR_c << std::endl;
  std::cout << "rmue forward = " << rmueCR_f << std::endl;
  std::cout << std::endl;
  std::cout << "R_T central = " << RTcr_c << std::endl;
  std::cout << "R_T forward = " << RTcr_f << std::endl;
  std::cout << std::endl;
  std::cout << setprecision(precision) << std::fixed;
  std::cout << "CR R(SF/OF) central = " << RSFcr_c << std::endl;
  std::cout << "CR R(ee/OF) central = " << Reecr_c << std::endl;
  std::cout << "CR R(mm/OF) central = " << Rmmcr_c << std::endl;
  std::cout << std::endl;
  std::cout << "CR R(SF/OF) forward = " << RSFcr_f << std::endl;
  std::cout << "CR R(ee/OF) forward = " << Reecr_f << std::endl;
  std::cout << "CR R(mm/OF) forward = " << Rmmcr_f << std::endl;

  //---------------------------------------------------------------------
  // Weighted average
  Observable RSF_c((RSFcr_c.v/(RSFcr_c.t2()) + Rsfof_c.v/(Rsfof_c.t2()))/(1./(RSFcr_c.t2()) + 1./(Rsfof_c.t2())));
  Observable Ree_c((Reecr_c.v/(Reecr_c.t2()) + ReeOF_c.v/(ReeOF_c.t2()))/(1./(Reecr_c.t2()) + 1./(ReeOF_c.t2())));
  Observable Rmm_c((Rmmcr_c.v/(Rmmcr_c.t2()) + RmmOF_c.v/(RmmOF_c.t2()))/(1./(Rmmcr_c.t2()) + 1./(RmmOF_c.t2())));

  Observable RSF_f((RSFcr_f.v/(RSFcr_f.t2()) + Rsfof_f.v/(Rsfof_f.t2()))/(1./(RSFcr_f.t2()) + 1./(Rsfof_f.t2())));
  Observable Ree_f((Reecr_f.v/(Reecr_f.t2()) + ReeOF_f.v/(ReeOF_f.t2()))/(1./(Reecr_f.t2()) + 1./(ReeOF_f.t2())));
  Observable Rmm_f((Rmmcr_f.v/(Rmmcr_f.t2()) + RmmOF_f.v/(RmmOF_f.t2()))/(1./(Rmmcr_f.t2()) + 1./(RmmOF_f.t2())));
  
  // Propagation of uncertainty
  RSF_c.e = sqrt( 1.0/( 1.0/(RSFcr_c.t()*RSFcr_c.t()) + 1.0/(Rsfof_c.t()*Rsfof_c.t()) ) );
  Ree_c.e = sqrt( 1.0/( 1.0/(Reecr_c.t()*Reecr_c.t()) + 1.0/(ReeOF_c.t()*ReeOF_c.t()) ) );
  Rmm_c.e = sqrt( 1.0/( 1.0/(Rmmcr_c.t()*Rmmcr_c.t()) + 1.0/(RmmOF_c.t()*RmmOF_c.t()) ) );
  
  RSF_f.e = sqrt( 1.0/( 1.0/(RSFcr_f.t()*RSFcr_f.t()) + 1.0/(Rsfof_f.t()*Rsfof_f.t()) ) );
  Ree_f.e = sqrt( 1.0/( 1.0/(Reecr_f.t()*Reecr_f.t()) + 1.0/(ReeOF_f.t()*ReeOF_f.t()) ) );
  Rmm_f.e = sqrt( 1.0/( 1.0/(Rmmcr_f.t()*Rmmcr_f.t()) + 1.0/(RmmOF_f.t()*RmmOF_f.t()) ) );
  
  std::cout << "=========================================" << std::endl;
  std::cout << "===         FINAL COMBINATION         ===" << std::endl;
  std::cout << "Final R(SF/OF) central = " << RSF_c <<  std::endl;
  std::cout << "Final R(ee/OF) central = " << Ree_c <<  std::endl;
  std::cout << "Final R(mm/OF) central = " << Rmm_c <<  std::endl;
  std::cout << std::endl;
  std::cout << "Final R(SF/OF) forward = " << RSF_f <<  std::endl;
  std::cout << "Final R(ee/OF) forward = " << Ree_f <<  std::endl;
  std::cout << "Final R(mm/OF) forward = " << Rmm_f <<  std::endl;
  std::cout << "=========================================" << std::endl;

  // For final calculations, only keep 2 significant digits
  RSF_c.roundUp(2);
  Ree_c.roundUp(2);
  Rmm_c.roundUp(2);
  RSF_f.roundUp(2);
  Ree_f.roundUp(2);
  Rmm_f.roundUp(2);

  // Take OF yield as statistical uncertainty, R(ll/OF) uncertainty as systematic
  int nEM_c = 750, nEM_f = 138;
  Observable nSFsr_c( RSF_c.v*nEM_c, sqrt(nEM_c)*RSF_c.v, RSF_c.e*nEM_c );
  Observable nEEsr_c( Ree_c.v*nEM_c, sqrt(nEM_c)*Ree_c.v, Ree_c.e*nEM_c );
  Observable nMMsr_c( Rmm_c.v*nEM_c, sqrt(nEM_c)*Rmm_c.v, Rmm_c.e*nEM_c );
  Observable nSFsr_f( RSF_f.v*nEM_f, sqrt(nEM_f)*RSF_f.v, RSF_f.e*nEM_f );
  Observable nEEsr_f( Ree_f.v*nEM_f, sqrt(nEM_f)*Ree_f.v, Ree_f.e*nEM_f );
  Observable nMMsr_f( Rmm_f.v*nEM_f, sqrt(nEM_f)*Rmm_f.v, Rmm_f.e*nEM_f );
  
  std::cout << std::setprecision(0);
  std::cout << "=========================================" << std::endl;
  std::cout << "===      FINAL ESTIMATE  (low mass)   ===" << std::endl;
  std::cout << "OF yield    central = " << nEM_c   <<  std::endl;
  std::cout << "FS estimate central = " << nSFsr_c <<  std::endl;
  std::cout << "EE estimate central = " << nEEsr_c <<  std::endl;
  std::cout << "MM estimate central = " << nMMsr_c <<  std::endl;
  std::cout << std::endl;
  std::cout << "OF yield    forward = " << nEM_f   <<  std::endl;
  std::cout << "FS estimate forward = " << nSFsr_f <<  std::endl;
  std::cout << "EE estimate forward = " << nEEsr_f <<  std::endl;
  std::cout << "MM estimate forward = " << nMMsr_f <<  std::endl;
  std::cout << "=========================================" << std::endl;
  
    int nEM_c = 371, nEM_f = 131;
  Observable nSFsr_c( RSF_c.v*nEM_c, sqrt(nEM_c)*RSF_c.v, RSF_c.e*nEM_c );
  Observable nEEsr_c( Ree_c.v*nEM_c, sqrt(nEM_c)*Ree_c.v, Ree_c.e*nEM_c );
  Observable nMMsr_c( Rmm_c.v*nEM_c, sqrt(nEM_c)*Rmm_c.v, Rmm_c.e*nEM_c );
  Observable nSFsr_f( RSF_f.v*nEM_f, sqrt(nEM_f)*RSF_f.v, RSF_f.e*nEM_f );
  Observable nEEsr_f( Ree_f.v*nEM_f, sqrt(nEM_f)*Ree_f.v, Ree_f.e*nEM_f );
  Observable nMMsr_f( Rmm_f.v*nEM_f, sqrt(nEM_f)*Rmm_f.v, Rmm_f.e*nEM_f );
  
  std::cout << std::setprecision(0);
  std::cout << "=========================================" << std::endl;
  std::cout << "===      FINAL ESTIMATE  (on Z)       ===" << std::endl;
  std::cout << "OF yield    central = " << nEM_c   <<  std::endl;
  std::cout << "FS estimate central = " << nSFsr_c <<  std::endl;
  std::cout << "EE estimate central = " << nEEsr_c <<  std::endl;
  std::cout << "MM estimate central = " << nMMsr_c <<  std::endl;
  std::cout << std::endl;
  std::cout << "OF yield    forward = " << nEM_f   <<  std::endl;
  std::cout << "FS estimate forward = " << nSFsr_f <<  std::endl;
  std::cout << "EE estimate forward = " << nEEsr_f <<  std::endl;
  std::cout << "MM estimate forward = " << nMMsr_f <<  std::endl;
  std::cout << "=========================================" << std::endl;
  
    int nEM_c = 785, nEM_f = 397;
  Observable nSFsr_c( RSF_c.v*nEM_c, sqrt(nEM_c)*RSF_c.v, RSF_c.e*nEM_c );
  Observable nEEsr_c( Ree_c.v*nEM_c, sqrt(nEM_c)*Ree_c.v, Ree_c.e*nEM_c );
  Observable nMMsr_c( Rmm_c.v*nEM_c, sqrt(nEM_c)*Rmm_c.v, Rmm_c.e*nEM_c );
  Observable nSFsr_f( RSF_f.v*nEM_f, sqrt(nEM_f)*RSF_f.v, RSF_f.e*nEM_f );
  Observable nEEsr_f( Ree_f.v*nEM_f, sqrt(nEM_f)*Ree_f.v, Ree_f.e*nEM_f );
  Observable nMMsr_f( Rmm_f.v*nEM_f, sqrt(nEM_f)*Rmm_f.v, Rmm_f.e*nEM_f );
  
  std::cout << std::setprecision(0);
  std::cout << "=========================================" << std::endl;
  std::cout << "===      FINAL ESTIMATE  (high mass)  ===" << std::endl;
  std::cout << "OF yield    central = " << nEM_c   <<  std::endl;
  std::cout << "FS estimate central = " << nSFsr_c <<  std::endl;
  std::cout << "EE estimate central = " << nEEsr_c <<  std::endl;
  std::cout << "MM estimate central = " << nMMsr_c <<  std::endl;
  std::cout << std::endl;
  std::cout << "OF yield    forward = " << nEM_f   <<  std::endl;
  std::cout << "FS estimate forward = " << nSFsr_f <<  std::endl;
  std::cout << "EE estimate forward = " << nEEsr_f <<  std::endl;
  std::cout << "MM estimate forward = " << nMMsr_f <<  std::endl;
  std::cout << "=========================================" << std::endl;

  
  
  return 0;
}
