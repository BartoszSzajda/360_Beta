import os
import glob
import pandas as pd
import csv
from Person import Assesed_Person
from Statistics import split_data
from Statistics import basic_statistics
from Statistics import calculating_cumulative_krippendorf
from Statistics import icc_mean_stats
from Statistics import top_bottom_five
from Statistics import biggest_gaps
from Statistics import all_items_means
from excel_pdf import create_excel_summary
from excel_pdf import chart_self_vs_other
from excel_pdf import chart_competences
from excel_pdf import chart_top_five
from excel_pdf import chart_bottom_five
from excel_pdf import draw_chart
from excel_pdf import pdf_essa
import krippendorff as kripp
import numpy as np
import pingouin as pg
from PyPDF2 import PdfWriter, PdfReader
import PyPDF2 as PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from PDF_combiner import PDFCombiner




RGB_values = {
    1: (68/255, 114/255, 196/255),
    2: (255/255, 192/255, 0/255),
    3: (165/255,165/255,165/255),
    4: (255/255,192/255,0/255)}

names =[]
df_mean = pd.DataFrame()

class CSVProcessor:
    def __init__(self,out_directory):
        self.out_directory = out_directory
        pass
    
    
    def process_csv(self, df, name, rgb_number):
        # Method to perform calculations on the CSV data
        # Example calculation on dataframe df
       
        
        person = Assesed_Person( data = df, split = None, basic_stats = None ,kripp_calc = None, 
                        icc_stats= None, icc_mean = None, icc_seperate_mean = None, top_five = None, bottom_five = None, top_five_diff = None, 
                        bottom_five_diff = None, item_mean = None,competences = None)
        
        print(f"Processing file with {len(df)} rows and {len(df.columns)} columns")
        person_split_inf= split_data(df)
        person.kripp_calc = calculating_cumulative_krippendorf(person_split_inf)
        person.kripp_calc = calculating_cumulative_krippendorf(person_split_inf)


        icc_mean_seperate_stats = icc_mean_stats(person_split_inf)
        person.icc_stats = icc_mean_seperate_stats[0]
        person.icc_mean = icc_mean_seperate_stats[1] # git sprawdzone 


        person.icc_seperate_mean = icc_mean_seperate_stats[2]


        top_bottom_5 = top_bottom_five(person_split_inf)
        person.top_five = top_bottom_5[0]
        person.bottom_five = top_bottom_5[1]

        biggest_gaps_ever = biggest_gaps(person_split_inf)
        person.top_five_diff = biggest_gaps_ever[0]
        person.bottom_five_diff = biggest_gaps_ever[1]

        person.item_mean = all_items_means(person_split_inf)
        
        
        create_excel_summary(person_split_inf,person.kripp_calc, person.icc_stats[0], person.icc_stats[1], person.icc_stats[2], person.icc_stats[3], person.icc_stats[4],
                     person.icc_mean, person.icc_seperate_mean, person.top_five, person.bottom_five, person.top_five_diff, person.bottom_five_diff, person.item_mean)
        
        self_vs_others = chart_self_vs_other(person.icc_mean,name, rgb_number)
        person.competences = chart_competences(person.icc_seperate_mean,name, rgb_number)
        top_five = chart_top_five(person.top_five_diff,name, rgb_number)
        bottom_five =chart_bottom_five(person.bottom_five_diff,name, rgb_number)
        
        names.append(name)
        #mean_df.insert(0,name,[person.icc_mean])
        
        #pdf_filename = f"{name}_output.pdf"  # Use the person's name for the file name
        #output_pdf_path = os.path.join(self.out_directory, pdf_filename)
        return person

def read_and_process_all_csv(directory_path):
    # Find all CSV files in the specified directory
    csv_files = glob.glob(os.path.join(directory_path, "*.csv"))
    df_mean =pd.DataFrame()
    
    RGB_values = [
     (68/255, 114/255, 196/255),
     (255/255, 192/255, 0/255),
     (165/255,165/255,165/255),
     (255/255,192/255,0/255)]
    
    processor = CSVProcessor('/Users/bartoszajda13/Desktop/360-beta')
    
    # Loop through all CSV files and process them
    for csv_file,value in zip(csv_files, RGB_values):
        print(f"Reading file: {csv_file}")
        df = pd.read_csv(csv_file)
        name = df['Imię i nazwisko osoby ocenianej'].iloc[0]
        person = processor.process_csv(df,name,value)
        df_mean[name] = person.competences
    
    #mean_df = pd.DataFrame(columns=[name for name in names ])
    pdf_files = [ "strona_startowa.pdf","strony_2_4.pdf", 
                f"chart_self_vs_other_{names[0]}.pdf", f"chart_competences_{names[0]}.pdf", f"chart_bottom_five_{names[0]}.pdf", f"chart_top_five_{names[0]}.pdf",
                f"chart_self_vs_other_{names[1]}.pdf", f"chart_competences_{names[1]}.pdf", f"chart_bottom_five_{names[1]}.pdf", f"chart_top_five_{names[1]}.pdf",
                f"chart_self_vs_other_{names[2]}.pdf", f"chart_competences_{names[2]}.pdf", f"chart_bottom_five_{names[2]}.pdf", f"chart_top_five_{names[2]}.pdf",
                f"chart_self_vs_other_{names[3]}.pdf", f"chart_competences_{names[3]}.pdf", f"chart_bottom_five_{names[3]}.pdf", f"chart_top_five_{names[3]}.pdf",
                "draw_chart_essa.pdf"]

    draw_chart(df_mean)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    combiner = PDFCombiner()
    combiner.combine_pdfs(pdf_files)
    
    #print(df_mean)
    


if __name__ == "__main__":
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Call the function to read and process all CSV files in the directory
    read_and_process_all_csv(script_dir)
