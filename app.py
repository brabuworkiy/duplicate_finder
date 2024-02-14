import streamlit as st
import pandas as pd


def remove_duplicates(df1, df2):
    # Remove duplicates from df1 and df2 individually
    df1_duplicates_removed = df1.drop_duplicates()
    df2_duplicates_removed = df2.drop_duplicates()

    # Concatenate the two dataframes and drop duplicates
    merged = pd.concat([df1_duplicates_removed, df2_duplicates_removed]).drop_duplicates(keep=False)
    return merged


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


if __name__ == "__main__":
    main()
