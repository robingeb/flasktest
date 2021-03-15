from fpdf import FPDF 

  
i = 5

pdf = FPDF() 
  
# Add a page 
pdf.add_page() 
  
# set style and size of font  
# that you want in the pdf 
pdf.set_font("Arial", size = 15) 
  
# create a cell 
pdf.cell(200, 10, txt = "Prüfbericht:",  
         ln = 1, align = 'C') 

# add another cell 
pdf.cell(200, 10, txt = "", 
         ln = 2, align = 'C') 

# add another cell 
pdf.cell(200, 10, txt = "aaölksdjfölaksdjfölkasjdf.", 
         ln = 2, align = 'C') 
  
# save the pdf with name .pdf 
pdf.output("Prüfbericht.pdf")    