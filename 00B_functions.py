################################################################################
# Pregnancy, Arsenic, and Immune Response (PAIR) Study
# Drinking Water Arsenic and Hemoglobin -- Functions

# Tyler Smith
# May 29, 2023

##### Function: tidy ###########################################################
# Define function `tidy` to gather model estimates in tidy data frame.
def tidy(models, names, x = ['ln_wAs_iqr','ln_wFe_iqr']):
    
    out = pd.DataFrame()

    name = 0
    
    for m in models:
        out_m = pd.DataFrame()
        out_m['est'] = m.params
        out_m['low'] = m.conf_int().iloc[:, 0]
        out_m['upp'] = m.conf_int().iloc[:, 1]
        out_m['pvl'] = m.pvalues
        out_m['mdl'] = names[name]

        out = pd.concat([out, out_m])
        
        name += 1

    out = out.reset_index(names = 'term')
    out = out[out['term'].isin(x)]

    return(out)
