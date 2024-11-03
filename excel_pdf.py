import pandas as pd
import krippendorff as kripp
import numpy as np
import pingouin as pg
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import textwrap
from matplotlib.backends.backend_pdf import PdfPages
import pdfkit
from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont 
import PyPDF2 as PyPDF2
from PyPDF2 import PdfWriter, PdfReader
import os 



#Excel summary

def create_excel_summary(basic_statistics, kripp_cumulative,icc_result_management, icc_result_result, icc_result_change,
                         icc_result_decision, icc_result_communication,mean_statistics, mean_separate_statistics,
                         top_five, bottom_five, top_five_diff, bottom_five_diff, item_mean_data):
    with pd.ExcelWriter("Analiza_danych_360_dla_XYZ.xlsx") as writer:
        basic_statistics.to_excel(writer, sheet_name="basic_statistics", index=True)
        kripp_cumulative.to_excel(writer, sheet_name="kripp_cumulative", index=True)
        icc_result_management.to_excel(writer, sheet_name="icc_result_management", index=True)
        icc_result_result.to_excel(writer, sheet_name="icc_result_result", index=True)
        icc_result_change.to_excel(writer, sheet_name="icc_result_change", index=True)
        icc_result_decision.to_excel(writer, sheet_name="icc_result_decision", index=True)
        icc_result_communication.to_excel(writer, sheet_name="icc_result_communication", index=True)
        mean_statistics.to_excel(writer, sheet_name="self_vs_other_perception", index=True)
        mean_separate_statistics.to_excel(writer, sheet_name="self_vs_other_sp_perception", index=True)
        top_five.to_excel(writer, sheet_name="your_top_5", index=True)
        bottom_five.to_excel(writer, sheet_name="your_bottom_5", index=True)
        top_five_diff.to_excel(writer, sheet_name="top_five_diff", index=True)
        bottom_five_diff.to_excel(writer, sheet_name="bottom_five_diff", index=True)
        item_mean_data.to_excel(writer, sheet_name="mean_and_score_every_item", index=True)
        
    
def chart_self_vs_other( mean_statistics,name,  RGB_badany):
    # Chart for self ve other perception
    # Reverse the order of columns in the DataFrame
   
    mean_statistics_reversed = mean_statistics.iloc[:, ::-1]

     #Create a PDF canvas
     
    output_dir = '/Users/bartoszajda13/Desktop/360_beta'
    file_path = os.path.join(output_dir, f"chart_self_vs_other_" +str(name)+".pdf")
    c = canvas.Canvas(file_path, pagesize=A4)
    
    
    

    # Set fill color to green
    c.setFillColorRGB(*RGB_badany)

    # Draw a filled rectangle in the top-left corner
    c.rect(0, 740, 270, 50, fill=1, stroke=0)
    c.rect(360, 740, 270, 50, fill=1, stroke=0)

    # Get the size of the canvas
    canvas_width, canvas_height = c._pagesize

    # Set font and size for the text
    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
    c.setFont("Verdana", 18)

    # Set color to white
    c.setFillColorRGB(1, 1, 1)

    # Define the word and its position
    word = "Średnie kompetencji"
    x = letter[0] - 240  # Distance from the right side
    y = letter[1] - 35   # Distance from the top

    # Draw the word on the canvas
    c.drawString(x, y, word)

    # Define the word and its position
    word = str(name)
    x = letter[0] - 600  # Distance from the right side
    y = letter[1] - 35   # Distance from the top

    # Draw the word on the canvas
    c.drawString(x, y, word)

    # Set color to green
    c.setFillColorRGB(143/255, 198/255, 62/255)

    c.setFont("Verdana", 10)

    # Define the words and their positions
    # Define the words and their positions
    words = ["Średnie kompetencji z podziałem na Samoocenę oraz oceny Sędziów zbiorczo – Skala (0-4)"]

    x = letter[0] - 680  # Distance from the right side
    y = letter[1] - 550   # Distance from the top

    # Draw the words on the canvas
    for word in words:
        lines = textwrap.wrap(word, width=100)  # Split text into lines
        for line in lines:
            c.drawString(x, y, line)  # Draw each line
            y -= 15  # Move to the next line

    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
    c.setFont("Verdana", 10)

    # Set color to black
    c.setFillColorRGB(0, 0, 0)

    # Get the value from the DataFrame
    # Highest value from "Ocena innych" rounded to two decimal places
    highest_mean_others = round(mean_statistics.filter(like='Ocena innych').max(axis=1)[0], 2)
    print(highest_mean_others)

    # Lowest value from "Ocena innych" rounded to two decimal places
    lowest_mean_others = round(mean_statistics.filter(like='Ocena innych').min(axis=1)[0], 2)

    # Highest value from "Samoocena" rounded to two decimal places
    highest_mean_self = round(mean_statistics.filter(like='Samoocena').max(axis=1)[0], 2)

    # Lowest value from "Samoocena" rounded to two decimal places
    lowest_mean_self = round(mean_statistics.filter(like='Samoocena').min(axis=1)[0], 2)

    # Define the words and their positions
    words2 = ["Powyższy wykres obrazuje wyniki badania z podziałem na samoocenę oraz ocenę sędziów w ramach 5 badanych kompetencji.",
            f"- Sędziowie najwyżej ocenili komunikacje ({highest_mean_others}), a najniżej zarządzanie zmianą ({lowest_mean_others})",
            f"- Najwyższa samoocena była przy kompetencji nastawienie na rezultat ({highest_mean_self}), a najniższa w komunikacji ({lowest_mean_self}). Samoocena jest zbliżona do oceny sędziów jednak odrobinę niższa"]

    x = letter[0] - 580  # Distance from the right side
    y = letter[1] - 475   # Distance from the top

    for word in words2:
        lines = textwrap.wrap(word, width=100)  # Split text into lines
        for line in lines:
            c.drawString(x, y, line)  # Draw each line
            y -= 15  # Move to the next line

    # Plotting a horizontal bar chart with custom size and extended x-axis
    fig, ax = plt.subplots(figsize=(12, 6))
    mean_statistics_reversed.T.plot(kind='barh', legend=None, ax=ax, zorder=3)
    plt.show

    # Extend x-axis
    ax.set_xlim(0, 4.5)
    ax.grid(axis='x', zorder=10, alpha=0.2)

    # Annotate bars with their values
    for i in ax.patches:
        plt.text(i.get_width(), i.get_y() + 0.1, str(round(i.get_width(), 2)), fontsize=9, color='black', ha='left')

    # Draw the chart on the canvas
    plt.tight_layout()
    plt.savefig("chart_self_vs_other_person_" + str(name)+ ".png", format="png")  # Save the chart as an image
    

    # Draw the chart on the canvas with custom size and location
    c.drawImage("chart_self_vs_other_person_" + str(name) + ".png", x=0, y=400, width=600, height=300)
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kropki.jpg')
    c.drawImage(fn, x=-60, y=-70, width=200, height=212.8)
    
   

    # Save the canvas as a PDF file
    
    c.save()
 
 
    
# Initialize an empty DataFrame with 4 columns
def chart_competences( mean_separate_statistics,name, RGB_badany):
    # Create a PDF canvas
    output_dir = '/Users/bartoszajda13/Desktop/360_beta'
    file_path = os.path.join(output_dir, f"chart_competences_" +str(name)+".pdf")
    c = canvas.Canvas(file_path, pagesize=A4)
    

    # Set fill color to green
    c.setFillColorRGB(*RGB_badany)

    # Draw a filled rectangle in the top-left corner
    c.rect(0, 740, 270, 50, fill=1, stroke=0)
    c.rect(360, 740, 270, 50, fill=1, stroke=0)

    # Get the size of the canvas
    canvas_width, canvas_height = c._pagesize

    # Set font and size for the text
    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
    c.setFont("Verdana", 18)

    # Set color to white
    c.setFillColorRGB(1, 1, 1)

    # Define the word and its position
    word = "Średnie kompetencji"
    x = letter[0] - 240  # Distance from the right side
    y = letter[1] - 35   # Distance from the top

    # Draw the word on the canvas
    c.drawString(x, y, word)

    # Define the word and its position
    word = str(name)
    x = letter[0] - 600  # Distance from the right side
    y = letter[1] - 35   # Distance from the top

    # Draw the word on the canvas
    c.drawString(x, y, word)

    # Set color to green
    c.setFillColorRGB(143/255, 198/255, 62/255)

    c.setFont("Verdana", 10)

    # Define the words and their positions
    # Define the words and their positions
    words = ["Średnie kompetencji z podziałem na Samoocenę oraz oceny Sędziów - Skala (0-4)"]

    x = letter[0] - 580  # Distance from the right side
    y = letter[1] - 450   # Distance from the top

    # Draw the words on the canvas
    for word in words:
        lines = textwrap.wrap(word, width=100)  # Split text into lines
        for line in lines:
            c.drawString(x, y, line)  # Draw each line
            y -= 15  # Move to the next line

    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
    c.setFont("Verdana", 10)

    # Set color to black
    c.setFillColorRGB(0, 0, 0)

    # Calculate the maximum value from each row and round to two decimal places
    max_values = mean_separate_statistics.apply(lambda row: round(row.max(), 2), axis=1)

    # Calculate the minimum value from each row and round to two decimal places
    min_values = mean_separate_statistics.apply(lambda row: round(row.min(), 2), axis=1)

    # Calculate the index of the maximum value from each row
    max_index = mean_separate_statistics.apply(lambda row: row.idxmax(), axis=1)

    # Calculate the index of the minimum value from each row
    min_index = mean_separate_statistics.apply(lambda row: row.idxmin(), axis=1)

    # Assign the maximum and minimum values to separate variables
    max_samoocena = max_values['Samoocena']
    max_index_samoocena = max_index['Samoocena']
    min_samoocena = min_values['Samoocena']
    min_index_samoocena = min_index['Samoocena']

    max_judge1 = max_values['Judge1']
    max_index_judge1 = max_index['Judge1']
    min_judge1 = min_values['Judge1']
    min_index_judge1 = min_index['Judge1']

    max_judge2 = max_values['Judge2']
    max_index_judge2 = max_index['Judge2']
    min_judge2 = min_values['Judge2']
    min_index_judge2 = min_index['Judge2']

    max_judge3 = max_values['Judge3']
    max_index_judge3 = max_index['Judge3']
    min_judge3 = min_values['Judge3']
    min_index_judge3 = min_index['Judge3']

    # Define the words and their positions
    words2 = ["Powyższy wykres obrazuje wyniki badania z podziałem na samoocenę oraz ocenę sędziów rozdzielnie w ramach 5 badanych kompetencji."
             f"- Sędzia 1 najwyżej ocenił kompetencje '{max_index_judge1}' ({max_judge1}), a najniżej '{min_index_judge1}' ({min_judge1}).",
             f"- Sędzia 2 najwyżej ocenił kompetencje '{max_index_judge2}' ({max_judge2}), a najniżej '{min_index_judge2}' ({min_judge2}).",
             f"- Sędzia 3 najwyżej ocenił kompetencje '{max_index_judge1}' ({max_judge1}), a najniżej '{min_index_judge1}' ({min_judge1}).",
             f"W ramach samooceny najwyżej oceniona została kompetencja '{max_index_samoocena}' ({max_samoocena}), a najniżej '{min_index_samoocena}' ({min_samoocena})."]


    x = letter[0] - 580  # Distance from the right side
    y = letter[1] - 475   # Distance from the top

    for word in words2:
        lines = textwrap.wrap(word, width=100)  # Split text into lines
        for line in lines:
            c.drawString(x, y, line)  # Draw each line
            y -= 15  # Move to the next line


    # Plotting a grouped bar chart with separation between bars
    fig, ax = plt.subplots(figsize=(15, 6))

    bar_width = 0.20
    index = np.arange(len(mean_separate_statistics.columns))

    # Custom colors for the bars
    colors = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000']

    for i, (index_value, row) in enumerate(mean_separate_statistics.iterrows()):
        ax.bar(index + i * bar_width, row, bar_width, label=index_value, color=colors[i], zorder=10)
        # Add values above each bar
        for j, value in enumerate(row):
            ax.text(index[j] + i * bar_width, value + 0.05, str(round(value, 2)), ha='center', va='bottom')

    ax.set_ylim(0, 4.5)
    ax.grid(axis='y', zorder=10, alpha=0.2)
    ax.set_xlabel('Categories')
    ax.set_xticks(index + bar_width * (len(mean_separate_statistics) - 1) / 2)
    ax.set_xticklabels(mean_separate_statistics.columns)

    # Move the legend to below the x-axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), shadow=True, ncol=len(mean_separate_statistics))

    # Draw the chart on the canvas
    plt.tight_layout()
    plt.savefig("chart_competences_person_"+ str(name)+".png", format="png")  # Save the chart as an image

    # Draw the chart on the canvas with custom size and location
    c.drawImage("chart_competences_person_"+ str(name)+".png", x=0, y=400, width=600, height=300)
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kropki.jpg')
    c.drawImage(fn, x=-60, y=-70, width=200, height=212.8)

    means = mean_separate_statistics.mean()
    
    # Save the canvas as a PDF file
    #dir_path = os.path.join('/Users/bartoszajda13/Desktop/360_beta',"chart_self_vs_other_person_"+name +".pdf")
    c.save()
    

    return means

    #means = chart_competences(numer_badanego)

    #mean_df[name_values.get(numer_badanego)] = means



def chart_top_five(top_five_diff,name,RGB_badany):
    # Define custom colors for each category
    custom_colors = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000']

    # Select columns 0, 1, 2, and 4 from the DataFrame
    top_five_diff_selected = top_five_diff.iloc[:, [0, 1, 2, 4]]

    # Reverse the order of columns in the DataFrame
    top_five_diff_selected = top_five_diff_selected.iloc[:, ::-1]

    # Create a PDF canvas
    output_dir = '/Users/bartoszajda13/Desktop/360_beta'
    file_path = os.path.join(output_dir, f"chart_top_five_" +str(name)+".pdf")
 
    c = canvas.Canvas(file_path, pagesize=A4)
    
   

    # Set fill color to green
    c.setFillColorRGB(*RGB_badany)

    # Draw a filled rectangle in the top-left corner
    c.rect(0, 740, 270, 50, fill=1, stroke=0)
    c.rect(360, 740, 270, 50, fill=1, stroke=0)

    # Get the size of the canvas
    canvas_width, canvas_height = c._pagesize

    # Set font and size for the text
    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
    c.setFont("Verdana", 18)

    # Set color to white
    c.setFillColorRGB(1, 1, 1)

    # Define the word and its position
    word = "5 zawyżonych ocen"
    x = letter[0] - 240  # Distance from the right side
    y = letter[1] - 35   # Distance from the top

    # Draw the word on the canvas
    c.drawString(x, y, word)

    # Define the word and its position
    word = str(name)
    x = letter[0] - 600  # Distance from the right side
    y = letter[1] - 35   # Distance from the top

    # Draw the word on the canvas
    c.drawString(x, y, word)

    # Set color to green
    c.setFillColorRGB(143/255, 198/255, 62/255)

    c.setFont("Verdana", 10)

    # Define the words and their positions
    # Define the words and their positions
    words = ["5 najbardziej zawyżonych samoocen w ocenie pomiędzy zebranymi ocenami - Skala (0-4)"]

    x = letter[0] - 580  # Distance from the right side
    y = letter[1] - 450   # Distance from the top

    # Draw the words on the canvas
    for word in words:
        lines = textwrap.wrap(word, width=100)  # Split text into lines
        for line in lines:
            c.drawString(x, y, line)  # Draw each line
            y -= 15  # Move to the next line

    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
    c.setFont("Verdana", 10)

    # Set color to black
    c.setFillColorRGB(0, 0, 0)

    # Get the value from the DataFrame
    value10 = top_five_diff.index[4]
    value11 = top_five_diff_selected.iloc[4, 0]
    value12 = top_five_diff_selected.iloc[4, 1]
    value13 = top_five_diff_selected.iloc[4, 2]
    value14 = top_five_diff_selected.iloc[4, 3]

    value20 = top_five_diff.index[3]
    value21 = top_five_diff_selected.iloc[3, 0]
    value22 = top_five_diff_selected.iloc[3, 1]
    value23 = top_five_diff_selected.iloc[3, 2]
    value24 = top_five_diff_selected.iloc[3, 3]

    value30 = top_five_diff.index[2]
    value31 = top_five_diff_selected.iloc[2, 0]
    value32 = top_five_diff_selected.iloc[2, 1]
    value33 =top_five_diff_selected.iloc[2, 2]
    value34 = top_five_diff_selected.iloc[2, 3]

    value40 = top_five_diff.index[1]
    value41 = top_five_diff_selected.iloc[1, 0]
    value42 = top_five_diff_selected.iloc[1, 1]
    value43 =top_five_diff_selected.iloc[1, 2]
    value44 = top_five_diff_selected.iloc[1, 3]

    value50 = top_five_diff.index[0]
    value51 = top_five_diff_selected.iloc[0, 0]
    value52 = top_five_diff_selected.iloc[0, 1]
    value53 =top_five_diff_selected.iloc[0, 2]
    value54 = top_five_diff_selected.iloc[0, 3]

    # Define the words and their positions
    words2 = ["Największe różnice wyniknęły w zachowaniu:",
            f"- „{value10}”, gdzie samoocena została oceniona na poziomie {value11}, a sędziowie ocenili na poziomie {value12}, {value13} i {value14}",
            f"- „{value20}” gdzie samoocena została oceniona na poziomie {value21}, a sędziowie ocenili na poziomie {value22}, {value23} i {value24}",
            f"- „{value30}”, gdzie samoocena została oceniona na poziomie {value31}, a sędziowie ocenili na poziomie {value32}, {value33} i {value34}",
            f"- „{value40}”, gdzie samoocena została oceniona na poziomie {value41}, a sędziowie ocenili na poziomie {value42}, {value43} i {value44}",
            f"- „{value50}”, gdzie samoocena została oceniona na poziomie {value51}, a sędziowie ocenili na poziomie {value52}, {value53} i {value54}"]


    x = letter[0] - 580  # Distance from the right side
    y = letter[1] - 475   # Distance from the top

    for word in words2:
        lines = textwrap.wrap(word, width=100)  # Split text into lines
        for line in lines:
            c.drawString(x, y, line)  # Draw each line
            y -= 15  # Move to the next line

    # Plotting grouped horizontal bar chart with custom size and extended x-axis
    fig, ax = plt.subplots(figsize=(10, 6))

    bar_width = 0.2  # Width of each bar
    n = len(top_five_diff_selected)  # Number of categories
    index = range(n)  # Index for positioning bars

    # Loop through each category and plot grouped bars
    legend_handles = []
    for i, (col_name, data) in enumerate(top_five_diff_selected.items()):
        position = [x + i * bar_width for x in index]  # Position for bars in each group
        bars = ax.barh(position, data, height=bar_width, label=col_name, color=custom_colors[i])
        legend_handles.append(bars[0])  # Append the first bar in each group for legend

    # Set the y-ticks and labels
    ax.set_yticks([i + (len(top_five_diff_selected.columns) - 1) * bar_width / 2 for i in index])
    ax.set_yticklabels(top_five_diff_selected.index)

    # Wrap the index labels into multiple lines
    wrapped_labels = [textwrap.fill(label, width=30) for label in top_five_diff_selected.index]
    ax.set_yticklabels(wrapped_labels)

    # Extend x-axis
    ax.set_xlim(0, 4.5)

    # Add grid
    ax.grid(axis='x', zorder=10, alpha=0.2)

    # Manually specify legend labels
    legend_labels = ['Judge1', 'Judge2', 'Judge3', 'Samoocena']

    # Create legend with color patches and manually specified labels
    legend_patches = [Patch(color=bar.get_facecolor(), label=label) for bar, label in zip(legend_handles[::-1], legend_labels)]

    # Place the legend below the chart
    ax.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=len(legend_labels))

    # Draw the chart on the canvas
    plt.tight_layout()
    plt.savefig("chart_top_five_person_"+ str(name)+".png", format="png")  # Save the chart as an image

    # Draw the chart on the canvas with custom size and location
    c.drawImage("chart_top_five_person_"+ str(name)+".png", x=0, y=370, width=550, height=330)
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kropki.jpg')
    c.drawImage(fn, x=-60, y=-70, width=200, height=212.8)

    # Save the canvas as a PDF file
    c.save()
    
def chart_bottom_five(bottom_five_diff, name, RGB_badany):
        # Define custom colors for each category
    custom_colors = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000']

    # Select columns 0, 1, 2, and 4 from the DataFrame
    bottom_five_diff_selected = bottom_five_diff.iloc[:, [0, 1, 2, 4]]

    # Reverse the order of columns in the DataFrame
    bottom_five_diff_selected = bottom_five_diff_selected.iloc[:, ::-1]

    # Create a PDF canvas
    output_dir = '/Users/bartoszajda13/Desktop/360_beta'
    file_path = os.path.join(output_dir, f"chart_bottom_five_" +str(name)+".pdf")
    c = canvas.Canvas(file_path, pagesize=A4)
    

    # Set fill color to green
    c.setFillColorRGB(*RGB_badany)

    # Draw a filled rectangle in the top-left corner
    c.rect(0, 740, 270, 50, fill=1, stroke=0)
    c.rect(360, 740, 270, 50, fill=1, stroke=0)

    # Get the size of the canvas
    canvas_width, canvas_height = c._pagesize

    # Set font and size for the text
    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
    c.setFont("Verdana", 18)

    # Set color to white
    c.setFillColorRGB(1, 1, 1)

    # Define the word and its position
    word = "5 zaniżonych ocen"
    x = letter[0] - 240  # Distance from the right side
    y = letter[1] - 35   # Distance from the top

    # Draw the word on the canvas
    c.drawString(x, y, word)

    # Define the word and its position
    word = str(name)
    x = letter[0] - 600  # Distance from the right side
    y = letter[1] - 35   # Distance from the top

    # Draw the word on the canvas
    c.drawString(x, y, word)

    # Set color to green
    c.setFillColorRGB(143/255, 198/255, 62/255)

    c.setFont("Verdana", 10)

    # Define the words and their positions
    # Define the words and their positions
    words = ["5 najbardziej zaniżonych samoocen w ocenie pomiędzy zebranymi ocenami - Skala (0-4)"]

    x = letter[0] - 580  # Distance from the right side
    y = letter[1] - 450   # Distance from the top

    # Draw the words on the canvas
    for word in words:
        lines = textwrap.wrap(word, width=100)  # Split text into lines
        for line in lines:
            c.drawString(x, y, line)  # Draw each line
            y -= 15  # Move to the next line

    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
    c.setFont("Verdana", 10)

    # Set color to black
    c.setFillColorRGB(0, 0, 0)

    # Get the value from the DataFrame
    value10 = bottom_five_diff.index[4]
    value11 = bottom_five_diff_selected.iloc[4, 0]
    value12 = bottom_five_diff_selected.iloc[4, 1]
    value13 = bottom_five_diff_selected.iloc[4, 2]
    value14 = bottom_five_diff_selected.iloc[4, 3]

    value20 = bottom_five_diff.index[3]
    value21 = bottom_five_diff_selected.iloc[3, 0]
    value22 = bottom_five_diff_selected.iloc[3, 1]
    value23 = bottom_five_diff_selected.iloc[3, 2]
    value24 = bottom_five_diff_selected.iloc[3, 3]

    value30 = bottom_five_diff.index[2]
    value31 = bottom_five_diff_selected.iloc[2, 0]
    value32 = bottom_five_diff_selected.iloc[2, 1]
    value33 =bottom_five_diff_selected.iloc[2, 2]
    value34 = bottom_five_diff_selected.iloc[2, 3]

    value40 = bottom_five_diff.index[1]
    value41 = bottom_five_diff_selected.iloc[1, 0]
    value42 = bottom_five_diff_selected.iloc[1, 1]
    value43 =bottom_five_diff_selected.iloc[1, 2]
    value44 = bottom_five_diff_selected.iloc[1, 3]

    value50 = bottom_five_diff.index[0]
    value51 = bottom_five_diff_selected.iloc[0, 0]
    value52 = bottom_five_diff_selected.iloc[0, 1]
    value53 =bottom_five_diff_selected.iloc[0, 2]
    value54 = bottom_five_diff_selected.iloc[0, 3]

    # Define the words and their positions
    words2 = ["Największe różnice wyniknęły w zachowaniu:",
            f"- „{value10}”, gdzie samoocena została oceniona na poziomie {value11}, a sędziowie ocenili na poziomie {value12}, {value13} i {value14}"
            f"- „{value20}” gdzie samoocena została oceniona na poziomie {value21}, a sędziowie ocenili na poziomie {value22}, {value23} i {value24}"
            f"- „{value30}”, gdzie samoocena została oceniona na poziomie {value31}, a sędziowie ocenili na poziomie {value32}, {value33} i {value34}"
            f"- „{value40}”, gdzie samoocena została oceniona na poziomie {value41}, a sędziowie ocenili na poziomie {value42}, {value43} i {value44}"
            f"- „{value50}”, gdzie samoocena została oceniona na poziomie {value51}, a sędziowie ocenili na poziomie {value52}, {value53} i {value54}"]


    x = letter[0] - 580  # Distance from the right side
    y = letter[1] - 475   # Distance from the top

    for word in words2:
        lines = textwrap.wrap(word, width=100)  # Split text into lines
        for line in lines:
            c.drawString(x, y, line)  # Draw each line
            y -= 15  # Move to the next line

    # Plotting grouped horizontal bar chart with custom size and extended x-axis
    fig, ax = plt.subplots(figsize=(10, 6))

    bar_width = 0.2  # Width of each bar
    n = len(bottom_five_diff_selected)  # Number of categories
    index = range(n)  # Index for positioning bars

    # Loop through each category and plot grouped bars
    legend_handles = []
    for i, (col_name, data) in enumerate(bottom_five_diff_selected.items()):
        position = [x + i * bar_width for x in index]  # Position for bars in each group
        bars = ax.barh(position, data, height=bar_width, label=col_name, color=custom_colors[i])
        legend_handles.append(bars[0])  # Append the first bar in each group for legend

    # Set the y-ticks and labels
    ax.set_yticks([i + (len(bottom_five_diff_selected.columns) - 1) * bar_width / 2 for i in index])
    ax.set_yticklabels(bottom_five_diff_selected.index)

    # Wrap the index labels into multiple lines
    wrapped_labels = [textwrap.fill(label, width=30) for label in bottom_five_diff_selected.index]
    ax.set_yticklabels(wrapped_labels)

    # Extend x-axis
    ax.set_xlim(0, 4.5)

    # Add grid
    ax.grid(axis='x', zorder=10, alpha=0.2)

    # Manually specify legend labels
    legend_labels = ['Judge1', 'Judge2', 'Judge3', 'Samoocena']

    # Create legend with color patches and manually specified labels
    legend_patches = [Patch(color=bar.get_facecolor(), label=label) for bar, label in zip(legend_handles[::-1], legend_labels)]

    # Place the legend below the chart
    ax.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=len(legend_labels))

    # Draw the chart on the canvas
    plt.tight_layout()
    plt.savefig("chart_bottom_five_person_"+ str(name)+".png", format="png")  # Save the chart as an image

    # Draw the chart on the canvas with custom size and location
    c.drawImage("chart_bottom_five_person_"+ str(name)+".png", x=0, y=370, width=550, height=330)
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kropki.jpg')
    c.drawImage(fn, x=-60, y=-70, width=200, height=212.8)

    # Save the canvas as a PDF file
    c.save()    


# Podsumowanie
# Initialize an empty DataFrame with 4 columns
def draw_chart( mean_df):
    # Create a PDF canvas
    
    
    output_dir = '/Users/bartoszajda13/Desktop/360_beta'
    file_path = os.path.join(output_dir, f"draw_chart_essa.pdf")
    c = canvas.Canvas(file_path, pagesize=A4)

    # Set font and size for the text
    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
    c.setFont("Verdana", 18)

    # Set color to white
    c.setFillColorRGB(1, 1, 1)

    # Define the word and its position
    word = "Średnie kompetencji"
    x = letter[0] - 240  # Distance from the right side
    y = letter[1] - 35   # Distance from the top

    # Draw the word on the canvas
    c.drawString(x, y, word)

    # Define the word and its position
    #word = name
    x = letter[0] - 600  # Distance from the right side
    y = letter[1] - 35   # Distance from the top

    # Draw the word on the canvas
    c.drawString(x, y, word)

    # Set color to green
    c.setFillColorRGB(143/255, 198/255, 62/255)

    c.setFont("Verdana", 10)

    # Define the words and their positions
    # Define the words and their positions
    words = ["Podsumowanie - Skala (0-4)"]

    x = letter[0] - 400  # Distance from the right side
    y = letter[1] - 450   # Distance from the top

    # Draw the words on the canvas
    for word in words:
        lines = textwrap.wrap(word, width=100)  # Split text into lines
        for line in lines:
            c.drawString(x, y, line)  # Draw each line
            y -= 15  # Move to the next line

    c.setFont("Verdana", 25)
    
    words = ["Podsumowanie"]

    x = letter[0] - 420  # Distance from the right side
    y = letter[1] - 50   # Distance from the top

    # Draw the words on the canvas
    for word in words:
        lines = textwrap.wrap(word, width=100)  # Split text into lines
        for line in lines:
            c.drawString(x, y, line)  # Draw each line
            y -= 15  # Move to the next line

    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
    c.setFont("Verdana", 10)

    # Set color to black
    c.setFillColorRGB(0, 0, 0)

    # Calculate the mean for each column
    column_means = mean_df.mean()

    # Sort the means in descending order
    sorted_means_people = column_means.sort_values(ascending=False)

    # Get the column names along with the mean values
    mean_values = sorted_means_people.values
    column_names = sorted_means_people.index

    # Assign each mean value to a separate variable
    mean1, column_name1 = round(mean_values[0], 2), column_names[0]
    mean2, column_name2 = round(mean_values[1], 2), column_names[1]
    mean3, column_name3 = round(mean_values[2], 2), column_names[2]
    mean4, column_name4 = round(mean_values[3], 2), column_names[3]

    # Calculate the mean for each row
    row_means = mean_df.mean(axis=1)

    # Sort the means in descending order
    sorted_means_competences = row_means.sort_values(ascending=False)

    # Get the row indices along with the mean values
    mean_values = sorted_means_competences.values
    row_indices = sorted_means_competences.index

    # Assign each mean value and corresponding row index to a separate variable
    mean5, row_index1 = round(mean_values[0], 2), row_indices[0]
    mean6, row_index2 = round(mean_values[1], 2), row_indices[1]
    mean7, row_index3 = round(mean_values[2], 2), row_indices[2]
    mean8, row_index4 = round(mean_values[3], 2), row_indices[3]

    # Define the words and their positions
    words2 = ["- Najwyżej ocenioną kompetencją w ramach całej grupy jest {} ({}), później {} ({}), następnie {} ({}) a najniżej {} ({}).".format(row_index1, mean5, row_index2, mean6, row_index3, mean7, row_index4, mean8),
             "- Najwyższe wyniki wśród badanych osiąga {} ({}), później {} ({}), a następnie {} ({}), a najniższe {} ({}).".format(column_name1, mean1, column_name2, mean2, column_name3, mean3, column_name4, mean4)]


    x = letter[0] - 580  # Distance from the right side
    y = letter[1] - 475   # Distance from the top

    for word in words2:
        lines = textwrap.wrap(word, width=100)  # Split text into lines
        for line in lines:
            c.drawString(x, y, line)  # Draw each line
            y -= 15  # Move to the next line


    # Plotting a grouped bar chart with separation between bars
    fig, ax = plt.subplots(figsize=(15, 6))

    bar_width = 0.1
    index = np.arange(len(mean_df.columns))

    # Custom colors for the bars
    colors = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5']

    for i, (index_value, row) in enumerate(mean_df.iterrows()):
        ax.bar(index + i * bar_width, row, bar_width, label=index_value, color=colors[i], zorder=10)
        # Add values above each bar
        for j, value in enumerate(row):
            ax.text(index[j] + i * bar_width, value + 0.05, str(round(value, 2)), ha='center', va='bottom')

    ax.set_ylim(0, 4.5)
    ax.grid(axis='y', zorder=10, alpha=0.2)
    ax.set_xlabel('Categories')
    ax.set_xticks(index + bar_width * (len(mean_df) - 1) / 2)
    ax.set_xticklabels(mean_df.columns)

    # Move the legend to below the x-axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), shadow=True, ncol=len(mean_df))

    # Draw the chart on the canvas
    plt.tight_layout()
    plt.savefig("podsumowanie.png", format="png")  # Save the chart as an image

    # Draw the chart on the canvas with custom size and location
    c.drawImage("podsumowanie.png", x=0, y=400, width=600, height=240)
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kropki.jpg')
    c.drawImage(fn, x=-60, y=-70, width=200, height=212.8)
    
    # Save the canvas as a PDF file
    c.save()



def pdf_essa(names):
        # List of PDF files in the desired order
    pdf_files = [ "/Users/bartoszajda13/Desktop/360_beta/strony_2_4.pdf", 
                f"chart_self_vs_other_{names[0]}.pdf", f"chart_competences_{names[0]}.pdf", f"chart_bottom_five_{names[0]}.pdf", f"chart_top_five_{names[0]}.pdf",
                f"chart_self_vs_other_{names[1]}.pdf", f"chart_competences_{names[1]}.pdf", f"chart_bottom_five_{names[1]}.pdf", f"chart_top_five_{names[1]}.pdf",
                f"chart_self_vs_other_{names[2]}.pdf", f"chart_competences_{names[2]}.pdf", f"chart_bottom_five_{names[2]}.pdf", f"chart_top_five_{names[2]}.pdf",
                f"chart_self_vs_other_{names[3]}.pdf", f"chart_competences_{names[3]}.pdf", f"chart_bottom_five_{names[3]}.pdf", f"chart_top_five_{names[3]}.pdf",
                "draw_chart_essa.pdf"]

    # Create a PDF writer object
    pdf_writer = PyPDF2.PdfWriter()

    # Iterate through the PDF files and append them to the writer object
    for pdf_file in pdf_files:
        with open(pdf_file, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)

    # Write the merged PDF to a file
    with open("Raport_360_dla_" + names[0] + "_" + names[1] + "_" + names[2] + "_" + names[3] + ".pdf", 'wb') as output_file:
        pdf_writer.write(output_file)
            

