#import seaborn as sns
#import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

st.title('Change Management')

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    cm_data = pd.read_excel(uploaded_file)

    # Grouping and plotting the number of changes by application
    changes_by_app = cm_data.groupby('Application').size().sort_values(ascending=False)
    plt.figure(figsize=(20, 6))
    bars = changes_by_app.plot(kind='bar', color='lightgreen', edgecolor='black', width=0.8)
    plt.title('Number of Changes by Application')
    plt.xlabel('Application')
    plt.ylabel('Number of Changes')
    plt.xticks(rotation=45)
    plt.tight_layout()
    for bar in bars.patches:
        plt.annotate(format(bar.get_height(), '.0f'), 
                     (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                     ha='center', va='center', 
                     size=12, xytext=(0, 5), 
                     textcoords='offset points')
    st.pyplot(plt)

    # Group by month and count changes
    cm_data['Actual Start Date'] = pd.to_datetime(cm_data['Actual Start Date'])
    cm_data['Actual Start Month'] = cm_data['Actual Start Date'].dt.strftime('%Y-%m')
    changes_by_month = cm_data.groupby('Actual Start Month').size()
    plt.figure(figsize=(10, 6))
    changes_by_month.plot(kind='line', marker='.', color='lightgreen', markerfacecolor='g', markersize=10)
    for i, count in enumerate(changes_by_month):
        plt.text(i, count, str(count), ha='center', va='bottom', fontsize=10, color='black')
    plt.title('Number of Changes in each Month')
    plt.xlabel('Actual Start Month')
    plt.ylabel('Number of Changes')
    plt.xticks(rotation=45)
    plt.grid(axis='y', alpha=0.75)
    plt.tight_layout()
    st.pyplot(plt)

    # Group by month and application, and count changes
    changes_by_month_app = cm_data.groupby(['Actual Start Month', 'Application']).size().unstack(fill_value=0)

    # List of applications for user to choose from
    applications_list = changes_by_month_app.columns.tolist()

    # Check if there are any plots before the dropdown
    if changes_by_app.empty or changes_by_month.empty or changes_by_month_app.empty:
        st.write("No data available to display.")
    else:
        # Count and plot changes by priority
        priority_counts = cm_data['Priority'].value_counts()
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
        sns.countplot(data=cm_data, x='Priority', order=priority_counts.index, ax=ax1)
        ax1.set_title('Count of Changes by Priority')
        ax1.set_xlabel('Priority')
        ax1.set_ylabel('Count')
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
        for p in ax1.patches:
            ax1.annotate(format(p.get_height(), '.0f'), 
                         (p.get_x() + p.get_width() / 2., p.get_height()), 
                         ha='center', va='center', 
                         xytext=(0, 9), 
                         textcoords='offset points')
        ax2.pie(priority_counts, labels=priority_counts.index, autopct='%1.1f%%')
        ax2.set_title('Distribution of Changes by Priority')
        ax2.axis('equal')
        plt.tight_layout()
        st.pyplot(fig)

        # Count and plot changes by classification
        classification_counts = cm_data['Classification'].value_counts()
        fig, axs = plt.subplots(1, 2, figsize=(18, 8))
        sns_barplot = sns.countplot(data=cm_data, x='Classification', order=classification_counts.index, ax=axs[0])
        axs[0].set_title('Count of Changes by Classification')
        axs[0].set_xlabel('Classification')
        axs[0].set_ylabel('Count')
        axs[0].tick_params(axis='x', rotation=45)
        for p in sns_barplot.patches:
            sns_barplot.annotate(format(p.get_height(), '.0f'), 
                                 (p.get_x() + p.get_width() / 2., p.get_height()), 
                                 ha='center', va='center', 
                                 xytext=(0, 9), 
                                 textcoords='offset points')
        axs[1].pie(classification_counts, labels=classification_counts.index, autopct='%1.1f%%')
        axs[1].set_title('Distribution of Changes by Classification')
        axs[1].axis('equal')
        plt.tight_layout()
        st.pyplot(fig)

        # Count and plot changes by status
        status_counts = cm_data['Status'].value_counts()
        fig, axs = plt.subplots(1, 2, figsize=(18, 8))
        sns_barplot_status = sns.countplot(data=cm_data, x='Status', order=status_counts.index, ax=axs[0])
        axs[0].set_title('Count of Changes by Status')
        axs[0].set_xlabel('Status')
        axs[0].set_ylabel('Count')
        axs[0].tick_params(axis='x', rotation=45)
        for p in sns_barplot_status.patches:
            sns_barplot_status.annotate(format(p.get_height(), '.0f'), 
                                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                                        ha='center', va='center', 
                                        xytext=(0, 9), 
                                        textcoords='offset points')
        axs[1].pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=140)
        axs[1].set_title('Distribution of Changes by Status')
        axs[1].axis('equal')
        plt.tight_layout()
        st.pyplot(fig)

        # Count and plot changes by type
        change_type_counts = cm_data['Type of Change'].value_counts()
        fig, axs = plt.subplots(1, 2, figsize=(18, 8))
        sns_barplot_type = sns.countplot(data=cm_data, x='Type of Change', order=change_type_counts.index, ax=axs[0])
        axs[0].set_title('Count of Changes by Type')
        axs[0].set_xlabel('Type of Change')
        axs[0].set_ylabel('Count')
        axs[0].tick_params(axis='x', rotation=45)
        for p in sns_barplot_type.patches:
            sns_barplot_type.annotate(format(p.get_height(), '.0f'), 
                                      (p.get_x() + p.get_width() / 2., p.get_height()), 
                                      ha='center', va='center', 
                                      xytext=(0, 9), 
                                      textcoords='offset points')
        axs[1].pie(change_type_counts, labels=change_type_counts.index, autopct='%1.1f%%', startangle=140)
        axs[1].set_title('Distribution of Changes by Type')
        axs[1].axis('equal')
        plt.tight_layout()
        st.pyplot(fig)

        # Dropdown for selecting application to plot
        app_to_plot = st.selectbox("Select an application to plot", applications_list)

        # Check if the entered application exists in the data
        if app_to_plot:
            if app_to_plot in changes_by_month_app.columns:
                # Plotting the line chart for the specified application
                plt.figure(figsize=(12, 8))
                plt.plot(changes_by_month_app.index, changes_by_month_app[app_to_plot], marker='o', linestyle='-')

                # Annotate each point with its count value
                for i, count in enumerate(changes_by_month_app[app_to_plot]):
                    plt.text(i, count, str(count), ha='center', va='bottom', fontsize=10, color='black')

                plt.title(f'Number of Changes over Time for {app_to_plot}')
                plt.xlabel('Actual Start Month')
                plt.ylabel('Number of Changes')
                plt.xticks(rotation=45)
                plt.grid(axis='y', alpha=0.75)
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.write(f"No data found for the application: {app_to_plot}")

        # Stratified sample based on priority
        sample_size = int(len(cm_data) * 0.25)
        stratified_sample = cm_data.groupby('Priority', group_keys=False).apply(lambda x: x.sample(frac=0.25))
        st.write("Sampled Data (25% stratified by priority):")
        st.dataframe(stratified_sample)
        # Option to download the stratified sample as a CSV file
        csv = stratified_sample.to_csv(index=False).encode('utf-8')
        st.download_button("Download Sampled Data as CSV", data=csv, file_name="Generated_Sample.csv", mime='text/csv')
