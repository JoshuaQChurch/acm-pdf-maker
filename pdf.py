from fpdf import FPDF
import pandas as pd
import datetime
import math
import os 
import argparse


class PDF(FPDF):
    def __init__(self, filepath=None, title_font_family = "Times", cell_font_family = "Times", 
                title_font_size = 20, cell_font_size = 25, title_height = 1, cell_height = 0.75,
                align = "C", output_path = "", non_member_pages = 3):

        super().__init__(orientation="P", unit="in", format="Letter")

        # Create data frame from supplied data file.  
        self.df = self.__create_df(filepath)

        # Set font size 
        self.title_font_family = title_font_family
        self.cell_font_family = cell_font_family

        # Set font size 
        self.title_font_size = title_font_size
        self.cell_font_size = cell_font_size 

        # Set cell size
        self.title_height = title_height
        self.cell_height = cell_height

        # Set text alignment
        self.align = align

        # Set output directory
        self.output_path = output_path 

        # Set number of non-member pages
        self.non_member_pages = non_member_pages


    # Create data frame from supplied data file
    def __create_df(self, filepath):

        # Verify the supplied file is a valid csv file
        filename = os.path.basename(filepath)
        extension = filename.rsplit('.')
        error = "%s is not a valid csv file." % filename

        if (len(extension) < 2):
            raise(error)

        extension = extension[-1]
        
        if (extension != "csv"):
            raise(error)
        
        return(pd.read_csv(filepath))
        
        
    # Create sign in sheet from provided .csv file. 
    def create_sign_in(self, event="", date="", sort_by = "Last Name"):

        title = "%s - %s" % (event, date)

        df = self.df 
        columns = df.columns 

        # Verify 'Last Name' and 'First Name' columns exist. 
        if "Last Name" not in columns or "First Name" not in columns:
            raise("Columns 'First Name' and/or 'Last Name' not in datafile.")

        if sort_by not in columns:
            raise("Argument '%s' not in datafile." % sort_by)

        # Remove NaN values from 'First Name' and 'Last Name' columns
        df = df.dropna(subset = ['First Name', 'Last Name'])

        # Sort dataframe by sort_by value
        df = df.sort_values(by=[sort_by])

        # Calculate pages required for the sign-in sheet. 
        # Height
        margin = 0.393701
        page_height = 11 - ( margin * 2 ) - self.title_height
        cells_per_page = math.floor( ( ( page_height / len(df) ) * len(df) ) / self.cell_height ) 
        
        # Account for the header
        # [ Last ][ First ][ Signature ]
        cells_per_page = cells_per_page - 2

        # Width
        page_width = 8.5 - ( margin * 2 ) 

        # ACM members
        names_mem = ( page_width * 0.5 ) / 2
        signature = page_width * 0.5

        # Non-ACM members
        names_non_mem = ( page_width * 0.4 ) / 2
        acm_member = ( page_width * 0.2 )
        email_address = ( page_width * 0.4 )


        # Create sign-in for ACM members
        for i in range(len(df)):
            row = df.iloc[i]

            last_name = row["Last Name"] 
            first_name = row["First Name"] 

            if ( i % cells_per_page == 0 ):
                self.add_page()

                # Title information
                self.set_font(family = self.title_font_family, style = "B", size = self.title_font_size)
                self.cell(w = 0, h = self.title_height, txt = title, border = 0, ln = 0, align = self.align)
                self.ln()

                # [ Last ][ First ][    Signature    ]
                self.set_font(family = self.cell_font_family, style = "B", size = self.cell_font_size)

                self.cell(w = names_mem, h = self.cell_height, txt = "Last Name",
                        border = 1, ln = 0, align = self.align)

                self.cell(w = names_mem, h = self.cell_height, txt = "First Name",
                        border = 1, ln = 0, align = self.align)

                self.cell(w = signature, h = self.cell_height, txt = "Signature",
                        border = 1, ln = 1, align = self.align)

            # [ Last ][ First ][    Signature    ]
            self.set_font(family = self.cell_font_family, style = "", size = self.cell_font_size)

            self.cell(w = names_mem, h = self.cell_height, txt = last_name,
                    border = 1, ln = 0, align = self.align)

            self.cell(w = names_mem, h = self.cell_height, txt = first_name,
                    border = 1, ln = 0, align = self.align)

            self.cell(w = signature, h = self.cell_height, txt = "",
                    border = 1, ln = 1, align = self.align)

        # Create Non-ACM member sign in
        for i in range(self.non_member_pages):

            self.add_page()

            # Title information
            self.set_font(family = self.title_font_family, style = "B", size = self.title_font_size)
            self.cell(w = 0, h = self.title_height, txt = title, border = 0, ln = 0, align = self.align)
            self.ln()

            # [ Last ][ First ][ ACM Member? ][ Work E-Email ]
            self.set_font(family = self.cell_font_family, style = "B", size = 11)

            self.cell(w = names_non_mem, h = 0.4, txt = "Last Name",
                    border = 1, ln = 0, align = self.align)

            self.cell(w = names_non_mem, h = 0.4, txt = "First Name",
                    border = 1, ln = 0, align = self.align)

            self.cell(w = acm_member, h = 0.4, txt = "ACM Member?(Y/N)",
                    border = 1, ln = 0, align = self.align)

            self.cell(w = email_address, h = 0.4, txt = "Work E-email",
                    border = 1, ln = 1, align = self.align)

            # Create 10 entries for members
            for i in range(10):
                # [ Last ][ First ][ ACM Member? ][ Work E-Email ]
                self.set_font(family = self.cell_font_family, style = "", size = self.cell_font_size)

                self.cell(w = names_non_mem, h = 0.75, txt = "",
                        border = 1, ln = 0, align = self.align)

                self.cell(w = names_non_mem, h = 0.75, txt = "",
                        border = 1, ln = 0, align = self.align)

                self.cell(w = acm_member, h = 0.75, txt = "",
                        border = 1, ln = 0, align = self.align)

                self.cell(w = email_address, h = 0.75, txt = "",
                        border = 1, ln = 1, align = self.align)

        self.output(name = os.path.join(self.output_path, "acm_sign_in.pdf"), dest = 'F')


# Parse the command line arguments.
def parser():

    parser = argparse.ArgumentParser(description="Create sign-in sheets for ACM-related events.")
    parser.add_argument("-i", "--input", help="filepath to the ACM chapter member list file", required=True)
    parser.add_argument("-e", "--event", help="name of the ACM event", default="< Event Name >", type=str)
    parser.add_argument("-d", "--date", help="date of the ACM event", default="< Event Date >", type=str)
    parser.add_argument("-tf", "--title-font", help="title font size", default=20, type=int)
    parser.add_argument("-cf", "--cell-font", help="cell font size", default=25, type=int)
    parser.add_argument("-nm", "--non-member", help="additional non member pages", default=3, type=int)
    parser.add_argument("-o", "--output", help="output path of the sign-in sheet", default="")

    return parser.parse_args()


if __name__ == "__main__":

    args = parser()

    pdf = PDF(filepath = args.input, title_font_size = args.title_font, cell_font_size = args.cell_font, 
                non_member_pages = args.non_member, output_path = args.output)
    
    pdf.create_sign_in(event = args.event, date = args.date)
