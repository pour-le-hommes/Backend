



def document_formulas(empty_func,func:str) -> None:

    if func=="TF-IDF":
        full_text = '''\\text{TF-IDF}(t,d) = TF(t,d) \\times IDF(t)'''

    elif func=="TF":
        full_text = '''TF(t,d) = \\frac{\\text{Number of times term }t\\text{ appears in document }d}{\\text{Total number of terms in document }d}'''
        
    elif func=="IDF":
        full_text = '''IDF(t) = \log\left(\\frac{\\text{Total number of documents}}{1 + \\text{Number of documents containing term } t}\\right)'''
        
    elif func=="PWZ":
        full_text = '''P(w|z) = \\frac{\\beta_w + n_w^{(z)}}{\sum_w'(\\beta_w' + n_w'^{(z)})}'''
        
    elif func=="PZD":
        full_text = '''P(z|d) = \\frac{\\alpha_w + n_w^{(d)}}{\sum_w'(\\alpha_z' + n_z'^{(d)})}'''
        
    elif func=="COSIM":
        full_text = '''\\text{Cosine Similarity}(A,B) = \\frac{A.B}{\|A\|.\|B\|}'''
    
    return full_text