################################################################################
# Pregnancy, Arsenic, and Immune Response (PAIR) Study
# Drinking Water Arsenic and Hemoglobin -- Functions

# Tyler Smith
# May 29, 2023

##### Function: tidy ###########################################################
def tidy(models, names, x = ['ln_wAs_iqr','ln_wFe_iqr']):
    """From list of models, puts estimates for covariates x in tidy DataFrame 
    with rows labeled from list of names."""
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

    return out

##### Function: get_diagnostics ################################################
def get_diagnostics(model):
    """For model, make data frame with diagnostic information. This function
    will be called by diagnostic_plots()."""
    df = pd.DataFrame()
    
    df['resid'] = model.resid
    df['fitted'] = model.fittedvalues
    
    return df

##### Function: diagnostic_plots ###############################################
def diagnostic_plots(model, name = None):
    """For model, generates standard diagnostic plots."""
    df = get_diagnostics(model)

    fig, axes = plt.subplots(1, 2)

    axes[0].axvline(x = 0, linestyle = '--', color = 'red')
    axes[1].axhline(y = 0, linestyle = '--', color = 'red')

    sns.kdeplot(ax = axes[0], data = df, x = 'resid', color = 'gray')
    sns.regplot(ax = axes[1], data = df, x = 'fitted', y = 'stand', 
        lowess = True, scatter_kws = {'color': 'gray', 'alpha': 0.4}, 
        line_kws = {'color': 'black'})

    if name != None:
        title = 'Diagnostic Plots: ' + name
    else:
        title = 'Diagnostic Plots'

    fig.suptitle(title)

    axes[0].set_title('Density Plot of Residuals')
    axes[1].set_title('Residuals vs Fitted')

    axes[0].set_xlabel('Residuals')
    axes[1].set_xlabel('Fitted Values')

    axes[0].set_ylabel('Density')
    axes[1].set_ylabel('Residuals')

    plt.show()

