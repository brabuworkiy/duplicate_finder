import streamlit as st
import pandas as pd

st.markdown("""
<style>
#baseButton-header {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)


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
