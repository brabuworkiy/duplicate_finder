import streamlit as st
import pandas as pd
import base64

st.set_page_config(
    page_title="workiy-LDF",
    page_icon="icon.png",  # Provide the path to your favicon image
)

hide_st_style = """
           <style>
           #MainMenu {Visibility: hidden;}
           footer {Visibility: hidden;}
           header {Visibility: hidden;}
           <style/>
        
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown("""

<style>
    [data-testid=stSidebar] {
        background-color: #ff000018;
        color:#ff000010;
      

    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .st-emotion-cache-taue2i {
        background-color: rgba(-255, -255, -255, 0.2); /* Adjust the alpha value (last parameter) to set transparency */
        border-radius: 8px; /* Optional: Add border-radius for a rounded look */
        color:white;
  
    }
    
   .st-emotion-cache-10trblm {
    position: relative; /* Ensure the element is positioned relatively */
    top: -160px; /* Adjust the top position */
}

    .st-emotion-cache-1aehpvj.e1bju1570,
.st-emotion-cache-16idsys.e1nzilvr5 {
    display: none !important;
}
    
    
    .st-emotion-cache-1aehpvj.e1bju1570 {
    display: none !important;
}
    
    .st-emotion-cache-6qob1r eczjsme3{
        background-color: rgba(-255, -255, -255, 0.2); /* Adjust the alpha value (last parameter) to set transparency */
        border-radius: 8px; /* Optional: Add border-radius for a rounded look */
        color:white;
  
  
    }
    
     .st-emotion-cache-16txtl3 eczjsme4{
        background-color: rgba(-255, -255, -255, 0.2); /* Adjust the alpha value (last parameter) to set transparency */
        border-radius: 8px; /* Optional: Add border-radius for a rounded look */
        color:white;
  
  
    }
    
   .st-emotion-cache-6qob1r eczjsme3{
       background-color: rgba(255, 255, 255, 0.2); /* Adjust the alpha value (last parameter) to set transparency */
        border-radius: 8px; /* Optional: Add border-radius for a rounded look */
        color:white;
  

}

    .st-emotion-cache-taue2i input,
    .st-emotion-cache-taue2i button {
        opacity: 0.8; /* Adjust the opacity of the input and button */
        color:"blue";
        color:black;
    }

    .st-emotion-cache-taue2i input:hover,
    .st-emotion-cache-taue2i button:hover {
        opacity: 1; /* Adjust the opacity when hovering over the input and button */
    }
    
  
    </style>
    """,
    unsafe_allow_html=True
)







def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    background-position: center;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


set_background('img.jpg')


def remove_duplicates(df1, df2):
    # Remove duplicates from df1 based on 'Email Address' column
    df1_duplicates_removed = df1.drop_duplicates(subset=['Email Address'])

    # Remove rows from df2 if email addresses match any in df1
    df2_filtered = df2[~df2['Email Address'].isin(df1_duplicates_removed['Email Address'])]

    # Remove duplicates from df2 itself based on 'Email Address' column
    df2_duplicates_removed = df2_filtered.drop_duplicates(subset=['Email Address'])

    return df2_duplicates_removed


def main():
    st.title('LEAD GENERATION DUPLICATE FINDER')
    st.sidebar.subheader("LEAD GENERATION DUPLICATE FINDER")

    st.sidebar.write("LEAD DATA BASE Excel file:")
    uploaded_file1 = st.sidebar.file_uploader("Choose a file", type=['xlsx'], key="uploader1")

    st.sidebar.write("GENERATED LEAD Excel file:")
    uploaded_file2 = st.sidebar.file_uploader("Choose a file", type=['xlsx'], key="uploader2")

    if uploaded_file1 is not None and uploaded_file2 is not None:
        df1 = pd.read_excel(uploaded_file1)
        df2 = pd.read_excel(uploaded_file2)

        st.write("LEAD DATA BASE:")
        st.write(df1)

        st.write("GENERATED LEAD:")
        st.write(df2)

        st.write("Comparing Data...")
        compared_df = remove_duplicates(df1, df2)

        if compared_df.empty:
            st.write("No duplicates found in the second uploaded data.")
        else:
            st.write("GENERATED LEAD without Duplicates:")
            st.write(compared_df)

            st.write("Download the GENERATED LEAD without Duplicates:")
            csv = compared_df.to_csv(index=False)
            st.download_button(
                label="Download Data as CSV",
                data=csv,
                file_name='GENERATED_LEAD_without_duplicates.csv',
                mime='text/csv')

        # Display summary table
        summary_data = {
            "Count of Duplicate": len(df2) - len(compared_df),
            "Count of Self Duplicate": len(df2) - len(df2.drop_duplicates(subset=['Email Address'])),
            "Count of Uploaded Generated Lead": len(df2),
            "Count after Removing Duplicates": len(compared_df)
        }
        summary_df = pd.DataFrame([summary_data])
        st.write("Summary:")
        st.dataframe(summary_df)


if __name__ == "__main__":
    main()
