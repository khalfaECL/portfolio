#
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#import plotly.figure_factory as ff
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_curve, precision_recall_curve,auc
from sklearn.metrics import precision_score, recall_score ,average_precision_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def main():
    st.title('Binary Classification web App \n developped by KHALFA Youssef')
    st.write('Colon cancer is a significant health concern worldwide. Early detection and diagnosis are crucial for improving patient outcomes.')
    st.write('This project explores the potential of machine learning to aid in the early identification of colon cancer using patient data and advanced algorithms.')
    #image = Image.open("C:\Users\Lenovo\Documents\GitHub\portfolio\111.png")
    st.image("C:\\Users\\Lenovo\\Documents\\GitHub\\portfolio\\project3\\lala.png", caption="Data analyst in your service")
    st.sidebar.title("Binary Classification Web App")
    #st.markdown("colon cancer prediction")
    st.sidebar.markdown("Colon cancer prediction ")
    
    @st.cache_data(persist=True)
    def load_data():
        data=pd.read_csv('C:\\Users\\Lenovo\\Documents\\GitHub\\portfolio\\project3\\colon_cancer.csv',sep=';')
        return data
        #label=LabelEncoder()
        #for col in data.columns:
         #   data[col]=label.fit_transform(data[col])
        #return data  
    metrics_definition = {
    'Accuracy': 'Accuracy is the proportion of correct predictions out of all predictions made. It is a measure of how well a model performs overall.',
    'Precision': 'Precision is the proportion of true positive predictions out of all positive predictions. It measures the accuracy of positive predictions.',
    'Recall': 'Recall, also known as sensitivity or true positive rate, is the proportion of true positive predictions out of all actual positive instances. It measures the ability of the model to identify positive instances.',
    'F1 Score': 'The F1 score is the harmonic mean of precision and recall. It provides a balanced measure of a model\'s performance, considering both precision and recall.',
    'ROC Curve': 'The ROC curve plots the true positive rate (recall) against the false positive rate (1 - specificity) for different classification thresholds. It helps visualize the trade-off between true positives and false positives.',
    'Precision-Recall Curve': 'The precision-recall curve plots precision against recall for different classification thresholds. It is useful when the positive class is rare or when false positives are more important than false negatives.',
    'Confusion Matrix': 'The confusion matrix is a table that summarizes the predictions made by a classification model. It shows the number of true positives, true negatives, false positives, and false negatives.',
    'Explained Variance': 'Explained variance is a measure of how much variance in the target variable is explained by the model. It is calculated as the ratio of the variance explained by the model to the total variance in the target variable.',
    'Principal Component Analysis (PCA)': 'PCA is a dimensionality reduction technique that transforms high-dimensional data into a lower-dimensional space while preserving the most important information. It helps in visualizing and understanding complex data relationships.',
}
    def tooltip_text(tooltip):
        html = f"""
    <div style="display: inline-block; position: relative;">
      <span style="cursor: help; color: #0073e6; font-size: 18px;">🔍</span>
      <div style="
          visibility: hidden;
          width: 280px;
          background-color: #555;
          color: #fff;
          text-align: center;
          border-radius: 5px;
          padding: 5px;
          position: absolute;
          z-index: 1;
          bottom: 125%; 
          left: 50%;
          margin-left: -80px;
          opacity: 0;
          transition: opacity 0.3s;">
        {tooltip}
        <div style="
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: #555 transparent transparent transparent;">
        </div>
      </div>
    </div>
    <style>
    div:hover > div {{
        visibility: visible !important;
        opacity: 1 !important;
    }}
    </style>
    """
        st.markdown(html, unsafe_allow_html=True)


     
    def principal_components_analysis(df):
        st.sidebar.subheader("Principal Components Analysis")
        n_components = st.sidebar.slider("Number of components", 1, len(df.columns),key="n_components")
        scaler=StandardScaler()
        dt=df.drop(['id_sample','tissue_status'],axis=1)
        data_scaled=scaler.fit_transform(dt)
        pca=PCA(n_components=n_components)
        principal_components=pca.fit_transform(data_scaled)
        explained_variance_ratio = pca.explained_variance_ratio_
        tooltip_text(metrics_definition['Explained Variance'])
        st.write("Explained Variance Ratio:", explained_variance_ratio)
        tooltip_text(metrics_definition['Principal Component Analysis (PCA)'])
        st.write("Principal Components:", principal_components)
        return principal_components,explained_variance_ratio,n_components
    
    def plot_pca(principal_components,explain_var,fig_list,n_components):
        st.subheader("Principal Components Analysis")
        status_df = df[['tissue_status']]
        princ_comp = pd.concat([pd.DataFrame(principal_components, columns=['PC{}'.format(i + 1) for i in range(n_components)]), status_df], axis=1)
        if 'scatter plot' in fig_list:
            
#plt.show() 
            #fig=plt.figure()
            #fig, ax = plt.subplots()
            #ax.set_title('Principal Components Analysis (scatter)')
            sns.pairplot(princ_comp, hue="tissue_status", palette={'tumoral': 'red', 'normal': 'blue'})
            
            #ax.scatter(principal_components[:, 0], principal_components[:, 1])
            #ax.set_xlabel('Principal Component 1')
            #ax.set_ylabel('Principal Component 2')
            
            st.pyplot(plt)
            
        if  'bar plot' in fig_list:
            composantes = np.arange(1, len(explain_var) + 1)
            fig,ax=plt.subplots()
            #plt.figure(figsize=(8, 6))
            ax.bar(composantes, explain_var, color='skyblue')
            #plt.bar(composantes, explain_var, color='skyblue')
            ax.set_title('Principal Components Analysis (bar)', fontsize=14)
            #plt.title('Principal Components Analysis (bar)', fontsize=14)
            ax.set_xlabel('Principal Components', fontsize=12)
            #plt.xlabel('principal components', fontsize=12)
            #plt.ylabel('eigen values', fontsize=12)
            ax.set_ylabel('Eigen values', fontsize=12)
            ax.set_xticks(composantes)
            #plt.xticks(composantes)
            st.pyplot(fig)
            #plt.show()
    @st.cache_data(persist=True)
    def split(df):
        #y=df['tissue_status']
        y=df['tissue_status'].map({'normal': 0, 'tumoral': 1})
        x=df.drop(columns=['tissue_status','id_sample'])
        x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=0)
        return x_train,x_test,y_train,y_test
        
    def plot_metrics(metrics_list):
        #fig,ax=plt.subplots()
        #ax.scatter([1,2,3],[1,2,3])
        #y_pred=model.predict(x_test)
    
            
        if 'Confusion Matrix' in metrics_list:
            
            #"""
            #fig=plt.figure()
            #st.subheader('Confusion Matrix')
            #confusion_matrix(y_test,y_pred)
            #st.pyplot(fig)"""
            cm = confusion_matrix(y_test, y_pred)#,labels=model.classes_ )#,pos_label='1')
            fig, ax = plt.subplots()
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax)
            ax.set_xlabel("Predicted labels")
            ax.set_ylabel("True labels")
            ax.set_title("Confusion Matrix")
            st.subheader('Confusion Matrix')
            tooltip_text(metrics_definition['Confusion Matrix'])
            st.pyplot(fig)    
        if 'ROC Curve' in metrics_list:
            #"""
            #fig=plt.figure()
            #st.subheader('ROC Curve')
            #confusion_matrix(y_test,y_pred)
            #st.pyplot(fig)
            #"""
            fpr, tpr, _ = roc_curve(y_test, y_pred)#,labels=["tumoral","normal"])#model.classes_ )#,pos_label='1')
            roc_auc = auc(fpr, tpr)
            
            fig, ax = plt.subplots()
            ax.plot(fpr, tpr, color='blue', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
            ax.plot([0, 1], [0, 1], color='gray', linestyle='--')  # Diagonal line for random guessing
            ax.set_xlim([0.0, 1.0])
            ax.set_ylim([0.0, 1.05])
            ax.set_xlabel('False Positive Rate')
            ax.set_ylabel('True Positive Rate')
            ax.set_title('Receiver Operating Characteristic (ROC)')
            ax.legend(loc="lower right")
        
            st.subheader('ROC Curve')
            tooltip_text(metrics_definition['ROC Curve'])
            st.pyplot(fig)
                    
        if 'Precision-Recall Curve' in metrics_list:
            precision, recall,_= precision_recall_curve(y_test, y_pred)#,labels=model.classes_ )#pos_label='1')
            avg_precision = average_precision_score(y_test, y_pred)
            
            fig, ax = plt.subplots()
            ax.plot(recall, precision, color='purple', lw=2, label=f'Average Precision = {avg_precision:.2f}')
            ax.set_xlabel('Recall')
            ax.set_ylabel('Precision')
            ax.set_title('Precision-Recall Curve')
            ax.legend(loc="lower left")
            
            st.subheader('Precision-Recall Curve')
            tooltip_text(metrics_definition['Precision-Recall Curve'])
            st.pyplot(fig) 
           
    df=load_data()
    if st.sidebar.checkbox("Show raw data", False):
        st.subheader("Genes feautures Data Set")
        st.write(df)
    if st.sidebar.checkbox("Show PCA", False):
        results=principal_components_analysis(df)
        principal_components,explained_var,n_components=results[0],results[1],results[2]
        fig_list=st.sidebar.multiselect('What to plot?',('scatter plot','bar plot'))
        if st.sidebar.button("Analyse"):
            plot_pca(principal_components,explained_var,fig_list,n_components)
    x_train,x_test,y_train,y_test=split(df)
    #class_names=["tumoral","normal"]
    class_names=["1","0"]
    st.sidebar.subheader('Choose Classifier')
    classifier=st.sidebar.selectbox("Classifier",("Support Vector Machine (SVM)","Logistic Regression","Random Forest"))
    scaler = StandardScaler()
    scaler.fit(x_train)
    x_train_scaled = scaler.transform(x_train)
    x_test_scaled = scaler.transform(x_test)
    if classifier == "Support Vector Machine (SVM)":
        st.sidebar.subheader("Model Hyperparameters")
        C=st.sidebar.number_input("C (Regularization parameter)",0.01,10.0,step=0.01,key='C')
        kernel=st.sidebar.radio("kernel",("rbf","linear","sigmoid"),key='kernel')
        gamma=st.sidebar.radio("Gamma (Kernel Coefficient)",("scale","auto"),key="gamma")

        metrics=st.sidebar.multiselect('What metrics to plot?',('Confusion Matrix','ROC Curve','Precision-Recall Curve'))

        if st.sidebar.button('Classify',key='classify'):
            st.subheader('Support Vector Machine (SVM) Results')
            model=SVC(kernel=kernel, random_state=42, probability=True,gamma=gamma,C=C)
            model.fit(x_train_scaled,y_train)
            accuracy=model.score(x_test_scaled,y_test)
            #y_pred=model.predict_proba(x_test)[:,1]
            y_pred=model.predict(x_test_scaled)
            st.write("Accuracy: ",accuracy,round(2))
            st.write("Precision ", precision_score(y_test,y_pred,labels=class_names).round(2))#model.classes_
            st.write("Recall; ",recall_score(y_test,y_pred,labels=class_names).round(2))#model.classes_
            plot_metrics(metrics)

    elif classifier == "Logistic Regression":
        st.sidebar.subheader("Model parameters")
        #C=st.sidebar.number_input("C (Regularization parameter)",0.01,10.0,step=0.01,key='C_LR')
        max_iter=st.sidebar.slider("Maximum number of iterations",100,500,key='max_iter')
        cv=st.sidebar.number_input("cv (Cross Validation)",2,10,step=1,key='cv')
        n_jobs=st.sidebar.selectbox("n_jobs",(None,-1,1,-2),key='n_jobs')
        random_state=st.sidebar.selectbox("Random State",(None,0,42,'other'),key='random_state')
        if random_state=='other':
            random_state=st.sidebar.number_input("custom Random State",0,2**32-1,key='custom_random_state')
        metrics=st.sidebar.multiselect('What metrics to plot?',('Confusion Matrix','ROC Curve','Precision-Recall Curve'))

        if st.sidebar.button('Classify',key='classify'):
            st.subheader('Logistic Regression CV Results')
            model=LogisticRegressionCV(random_state=random_state,n_jobs=n_jobs,verbose=0,max_iter=max_iter,cv=cv)
            model.fit(x_train_scaled,y_train)
            accuracy=model.score(x_test_scaled,y_test)
            #y_pred=model.predict_proba(x_test_scaled)[:,1]
            y_pred=model.predict(x_test_scaled)
            st.write("Accuracy: ",accuracy,round(2))
            st.write("Precision ", precision_score(y_test,y_pred,labels=class_names).round(2))
            st.write("Recall; ",recall_score(y_test,y_pred,labels=class_names).round(2))
            plot_metrics(metrics)    
    
    elif classifier=="Random Forest":
        st.sidebar.subheader("Model parameters")
        n_estimators=st.sidebar.number_input("Number of trees in the forest",100,1000,step=100,key='n_estimators')
        max_depth=st.sidebar.selectbox("Maximum depth of the tree",(None,1,2,3,4,5,6,7,8,9,10),key='max_depth')
        min_samples_split=st.sidebar.selectbox("Minimum number of samples required to split an internal node",(2,3,4,5,6,7,8,9,10),key='min_samples_split')
        min_samples_leaf=st.sidebar.selectbox("Minimum number of samples required to be at a leaf node",(1,2,3,4,5,6,7,8,9,10),key='min_samples_leaf')
        random_state=st.sidebar.selectbox("Random State",(None,0,42,'other'),key='random_state')
        if random_state=='other':
            random_state=st.sidebar.number_input("custom Random State",0,2**32-1,key='custom_random_state')
        metrics=st.sidebar.multiselect('What metrics to plot?',('Confusion Matrix','ROC Curve','Precision-Recall Curve'))
        if st.sidebar.button('Classify',key='classify'):
            st.subheader('Random Forest Results')
            model=RandomForestClassifier(n_estimators=n_estimators,max_depth=max_depth,min_samples_split=min_samples_split,min_samples_leaf=min_samples_leaf,random_state=random_state)
            model.fit(x_train_scaled,y_train)
            accuracy=model.score(x_test_scaled,y_test)
            #y_pred=model.predict_proba(x_test_scaled)[:,1]
            y_pred=model.predict(x_test_scaled)
            st.write("Accuracy: ",accuracy,round(2))
            st.write("Precision ", precision_score(y_test,y_pred,labels=class_names).round(2))
            st.write("Recall; ",recall_score(y_test,y_pred,labels=class_names).round(2))
            plot_metrics(metrics)


if __name__ == '__main__':
    main()

