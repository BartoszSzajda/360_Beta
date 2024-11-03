
#create an assesed person object
class Assesed_Person:
    def __init__(self ,data,split, basic_stats, kripp_calc, icc_stats, icc_mean, icc_seperate_mean,top_five, bottom_five , 
                 top_five_diff, bottom_five_diff, item_mean, competences ):
        #self.name = name
        self.data = data
        self.split = split
        self.basic_stats = basic_stats
        self.kripp_calc = kripp_calc
        self.icc_stats = icc_stats
        self.icc_mean = icc_mean
        self.icc_seperate_mean = icc_seperate_mean
        self.top_five = top_five
        self.bottom_five = bottom_five
        self.top_five_diff = top_five_diff
        self.bottom_five_diff = bottom_five_diff
        self.item_mean = item_mean
        self.competences = competences
