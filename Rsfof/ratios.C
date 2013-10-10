//
// Macro to get the R_sf/of ratios and corresponding uncertainties
//
// Run as: root -l -q -b ratios.C
//

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

  friend ostream &operator <<(ostream &, const string &);
  
};

ostream &operator<<(ostream &stream, const Observable &o)
{
  return(stream << o.v << "+-" << o.e << "+-" << o.s << " (total unc. " << o.t() << " [" << o.t()/o.v*100. << "%])");
}


void getEffError(int num, int den, float& eff, float& err) { 
  eff = num/static_cast<float>(den);
  float up = TEfficiency::ClopperPearson(den,num,0.68,true) - eff;
  float down = -TEfficiency::ClopperPearson(den,num,0.68,false) + eff;
  err = TMath::Max(up,down);
  std::cout << eff << " " << err << std::endl;
}

float getRmueAndError(int a, int b, float& r, float& err) { 
  r   = sqrt(a/static_cast<float>(b)); 
  err = 0.5*r*sqrt(1/float(a)+1/float(b));
}

float getRTAndError(int ee, int mm, int em, float& RT, float& err) { 
  RT   = 2.0*sqrt(ee*mm)/static_cast<float>(em); 
  err = RT*sqrt(1/float(4.0*ee)+1/float(4.0*mm)+1/float(em));
}

float getRatioAndError(int a, int b, float& r, float& err) { 
  r   = a/static_cast<float>(b); 
  err = r*sqrt(1/float(a)+1/float(b));
}

float getRsfofFromRmueAndErr(float r, float er, float& rsfof, float& err ) { 
  rsfof =  0.5*(r+1.0/r);
  err = 0.5*( 1.0 - 1.0/(r*r)  )*er;
}

float getRelTrigErr(float EE, float MM, float EM, float errEE, float errMM, float errEM) { 
  // separate uncertainty for each trigger
  return sqrt((errEE*errEE)/(4*EE*EE*MM*MM)+(errMM*errMM)/(4*EE*EE*MM*MM) + (errEM*errEM)/(EM*EM)); 
}

float getRelTrigErr(float ee, float mm, float em, float relErr) { 
  // in the case of uniform relative uncertainty
  return getRelTrigErr(ee,mm,em,relErr*ee,relErr*mm,relErr*em);
}



//_________________________________________________________________________________
int ratios(void) {

  //---------------------------------------------------------------------
  // 1. R(SF/OF) from R_mue and trigger eff.

  //-- R(SF/OF) from R_mue
  Observable rmue_c; //1.101,0.0); rmue_c.s = rmue_c.v*0.10; // Neglect stat. unc. <--- CHECK
  Observable rmue_f; //1.209,0.0); rmue_f.s = rmue_f.v*0.20; // Neglect stat. unc. <--- CHECK
  getRmueAndError(45745,38585,rmue_c.v,rmue_c.e);
  getRmueAndError(28964,20530,rmue_f.v,rmue_f.e);
//  getRmueAndError(45476,38364,rmue_c.v,rmue_c.e);
//  getRmueAndError(28765,20429,rmue_f.v,rmue_f.e);
  rmue_c.s = rmue_c.v*0.10;
  rmue_f.s = rmue_f.v*0.20;
  
  Observable rsfof_rmue_c, rsfof_rmue_f;
  getRsfofFromRmueAndErr(rmue_c.v,rmue_c.s,rsfof_rmue_c.v,rsfof_rmue_c.s);
  getRsfofFromRmueAndErr(rmue_f.v,rmue_f.s,rsfof_rmue_f.v,rsfof_rmue_f.s);

  //-- R(SF/OF) for trigger eff.
  int kEE_c = 1238, nEE_c = 1278, kMM_c = 237, nMM_c = 243, kEM_c = 86, nEM_c = 89;
  int kEE_f =  337, nEE_f =  346, kMM_f =  85, nMM_f =  89, kEM_f = 22, nEM_f = 25;

  float srtrig_c = 0.05; // Relative systematic uncertainty
  float srtrig_f = 0.05;
  
  float trigEE_c, trigMM_c, trigEM_c, etrigEE_c, etrigMM_c, etrigEM_c;
  float trigEE_f, trigMM_f, trigEM_f, etrigEE_f, etrigMM_f, etrigEM_f;

  getEffError(kEE_c,nEE_c,trigEE_c,etrigEE_c);
  getEffError(kMM_c,nMM_c,trigMM_c,etrigMM_c);
  getEffError(kEM_c,nEM_c,trigEM_c,etrigEM_c);

  getEffError(kEE_f,nEE_f,trigEE_f,etrigEE_f);
  getEffError(kMM_f,nMM_f,trigMM_f,etrigMM_f);
  getEffError(kEM_f,nEM_f,trigEM_f,etrigEM_f);
  
  Observable RT_c(sqrt(trigEE_c*trigMM_c)/trigEM_c);
  RT_c.e = RT_c.v*getRelTrigErr(trigEE_c,trigMM_c,trigEM_c,etrigEE_c,etrigMM_c,etrigEM_c);
  RT_c.s = RT_c.v*getRelTrigErr(trigEE_c,trigMM_c,trigEM_c,srtrig_c);

  Observable RT_f(sqrt(trigEE_f*trigMM_f)/trigEM_f);
  RT_f.e = RT_f.v*getRelTrigErr(trigEE_f,trigMM_f,trigEM_f,etrigEE_f,etrigMM_f,etrigEM_f);
  RT_f.s = RT_f.v*getRelTrigErr(trigEE_f,trigMM_f,trigEM_f,srtrig_f);
  

  //-- Folding them together
  Observable Rsfof_c(rsfof_rmue_c.v*RT_c.v);
  Rsfof_c.e  = sqrt(rsfof_rmue_c.e*rsfof_rmue_c.e+RT_c.e*RT_c.e);
  Rsfof_c.s  = sqrt(rsfof_rmue_c.s*rsfof_rmue_c.s+RT_c.s*RT_c.s);
  Observable Rsfof_f(rsfof_rmue_f.v*RT_f.v);
  Rsfof_f.e  = sqrt(rsfof_rmue_f.e*rsfof_rmue_f.e+RT_f.e*RT_f.e); 
  Rsfof_f.s  = sqrt(rsfof_rmue_f.s*rsfof_rmue_f.s+RT_f.s*RT_f.s);
  
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
  std::cout << setprecision(4) << std::fixed;
  std::cout << "rmue central = " << rmue_c << std::endl;
  std::cout << "rmue forward = " << rmue_f << std::endl;
  std::cout << "rsfof from rmue central = " << rsfof_rmue_c << std::endl;
  std::cout << "rsfof from rmue forward = " << rsfof_rmue_f << std::endl;
  std::cout << std::endl;
  std::cout << "R_T central = " << RT_c << std::endl;
  std::cout << "R_T forward = " << RT_f << std::endl;
  std::cout << std::endl;
  std::cout << setprecision(4) << std::fixed;
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
  
  int nEM = 390, nEE = 184, nMM = 210;
  getRatioAndError(nEE+nMM,nEM,RSFcr_c.v,RSFcr_c.e);
  RSFcr_c.s = RSFcr_c.v*0.02; // Syst. unc. from MC closure
  getRatioAndError(nEE,nEM,Reecr_c.v,Reecr_c.e);
  Reecr_c.s = Reecr_c.v*0.02; // Syst. unc. from MC closure
  getRatioAndError(nMM,nEM,Rmmcr_c.v,Rmmcr_c.e);
  Rmmcr_c.s = Rmmcr_c.v*0.02; // Syst. unc. from MC closure
  
  getRmueAndError(nMM,nEE,rmueCR_c.v,rmueCR_c.e);
  getRTAndError(nEE,nMM,nEM,RTcr_c.v,RTcr_c.e);

  nEM = 97, nEE = 40, nMM = 52;
  getRatioAndError(nEE+nMM,nEM,RSFcr_f.v,RSFcr_f.e);
  RSFcr_f.s = RSFcr_f.v*0.03; // Syst. unc. from MC closure
  getRatioAndError(nEE,nEM,Reecr_f.v,Reecr_f.e);
  Reecr_f.s = Reecr_f.v*0.04; // Syst. unc. from MC closure
  getRatioAndError(nMM,nEM,Rmmcr_f.v,Rmmcr_f.e);
  Rmmcr_f.s = Rmmcr_f.v*0.04; // Syst. unc. from MC closure

  getRmueAndError(nMM,nEE,rmueCR_f.v,rmueCR_f.e);
  getRTAndError(nEE,nMM,nEM,RTcr_f.v,RTcr_f.e);

  
  std::cout << "-----------------------------------------" << std::endl;
  std::cout << "--        SUMMARY CONTROL REGION       --" << std::endl;
  std::cout << setprecision(4) << std::fixed;
  std::cout << "rmue central = " << rmueCR_c << std::endl;
  std::cout << "rmue forward = " << rmueCR_f << std::endl;
  std::cout << std::endl;
  std::cout << "R_T central = " << RTcr_c << std::endl;
  std::cout << "R_T forward = " << RTcr_f << std::endl;
  std::cout << std::endl;
  std::cout << setprecision(4) << std::fixed;
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
  std::cout << sqrt(1.0/(1.0/(RSFcr_c.t()*RSFcr_c.t()) + 1.0/(Rsfof_c.t()*Rsfof_c.t()) ) ) << std::endl;
  
  RSF_c.e = sqrt(1.0/(1.0/(RSFcr_c.e*RSFcr_c.e) + 1.0/(Rsfof_c.e*Rsfof_c.e) ) );
  Ree_c.e = sqrt(1.0/(1.0/(Reecr_c.e*Reecr_c.e) + 1.0/(RmmOF_c.e*RmmOF_c.e) ) );
  Rmm_c.e = sqrt(1.0/(1.0/(Rmmcr_c.e*Rmmcr_c.e) + 1.0/(ReeOF_c.e*ReeOF_c.e) ) );

  RSF_c.s = sqrt(1.0/(1.0/(RSFcr_c.s*RSFcr_c.s) + 1.0/(Rsfof_c.s*Rsfof_c.s) ) );
  Ree_c.s = sqrt(1.0/(1.0/(Reecr_c.s*Reecr_c.s) + 1.0/(RmmOF_c.s*RmmOF_c.s) ) );
  Rmm_c.s = sqrt(1.0/(1.0/(Rmmcr_c.s*Rmmcr_c.s) + 1.0/(ReeOF_c.s*ReeOF_c.s) ) );

  RSF_f.e = sqrt(1.0/(1.0/(RSFcr_f.e*RSFcr_f.e) + 1.0/(Rsfof_f.e*Rsfof_f.e) ) );
  Ree_f.e = sqrt(1.0/(1.0/(Reecr_f.e*Reecr_f.e) + 1.0/(RmmOF_f.e*RmmOF_f.e) ) );
  Rmm_f.e = sqrt(1.0/(1.0/(Rmmcr_f.e*Rmmcr_f.e) + 1.0/(ReeOF_f.e*ReeOF_f.e) ) );
  
  RSF_f.s = sqrt(1.0/(1.0/(RSFcr_f.s*RSFcr_f.s) + 1.0/(Rsfof_f.s*Rsfof_f.s) ) );
  Ree_f.s = sqrt(1.0/(1.0/(Reecr_f.s*Reecr_f.s) + 1.0/(RmmOF_f.s*RmmOF_f.s) ) );
  Rmm_f.s = sqrt(1.0/(1.0/(Rmmcr_f.s*Rmmcr_f.s) + 1.0/(ReeOF_f.s*ReeOF_f.s) ) );
  
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
  
  
  return 0;
}
