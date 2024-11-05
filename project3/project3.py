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


def main():
    st.title('Binary Classification web App')
    st.sidebar.title("Binary Classification Web App")
    st.markdown("Are you edible or poisonus? ")
    st.sidebar.markdown("Are you edible or poisonus? ")
    
    @st.cache_data(persist=True)
    def load_data():
        data=pd.read_csv('E:\edu\ecc-materials\/2A\personal_projects\data\project3\mushrooms.csv')
        label=LabelEncoder()
        for col in data.columns:
            data[col]=label.fit_transform(data[col])
        return data   

    @st.cache_data(persist=True)
    def split(df):
        y=df.type
        x=df.drop(columns=['type'])
        x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=0)
        return x_train,x_test,y_train,y_test
    
    def plot_metrics(metrics_list):
        #fig,ax=plt.subplots()
        #ax.scatter([1,2,3],[1,2,3])
        y_pred=model.predict(x_test)
        
        if 'Confusion Matrix' in metrics_list:
            #"""
            #fig=plt.figure()
            #st.subheader('Confusion Matrix')
            #confusion_matrix(y_test,y_pred)
            #st.pyplot(fig)"""
            cm = confusion_matrix(y_test, y_pred)
            fig, ax = plt.subplots()
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax)
            ax.set_xlabel("Predicted labels")
            ax.set_ylabel("True labels")
            ax.set_title("Confusion Matrix")
            st.subheader('Confusion Matrix')
            st.pyplot(fig)    
        if 'ROC Curve' in metrics_list:
            #"""
            #fig=plt.figure()
            #st.subheader('ROC Curve')
            #confusion_matrix(y_test,y_pred)
            #st.pyplot(fig)
            #"""
            fpr, tpr, _ = roc_curve(y_test, y_pred)
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
            st.pyplot(fig)
                    
        if 'Precision-Recall Curve' in metrics_list:
            precision, recall, _ = precision_recall_curve(y_test, y_pred)
            avg_precision = average_precision_score(y_test, y_pred)
            
            fig, ax = plt.subplots()
            ax.plot(recall, precision, color='purple', lw=2, label=f'Average Precision = {avg_precision:.2f}')
            ax.set_xlabel('Recall')
            ax.set_ylabel('Precision')
            ax.set_title('Precision-Recall Curve')
            ax.legend(loc="lower left")
            
            st.subheader('Precision-Recall Curve')
            st.pyplot(fig) 
           
    df=load_data()
    x_train,x_test,y_train,y_test=split(df)
    class_names=['edible','poisonus']
    st.sidebar.subheader('Choose Classifier')
    classifier=st.sidebar.selectbox("Classifier",("Support Vector Machine (SVM)","Logistic Regression","Random Forest"))
    if classifier == "Support Vector Machine (SVM)":
        st.sidebar.subheader("Model Hyperparameters")
        C=st.sidebar.number_input("C (Regularization parameter)",0.01,10.0,step=0.01,key='C')
        kernel=st.sidebar.radio("kernel",("rbf","linear"),key='kernel')
        gamma=st.sidebar.radio("Gamma (Kernel Coefficient)",("scale","auto"),key="gamma")

        metrics=st.sidebar.multiselect('What metrics to plot?',('Confusion Matrix','ROC Curve','Precision-Recall Curve'))

        if st.sidebar.button('Classify',key='classify'):
            st.subheader('Support Vector Machine (SVM) Results')
            model=SVC(C=C,kernel=kernel,gamma=gamma)
            model.fit(x_train,y_train)
            accuracy=model.score(x_test,y_test)
            y_pred=model.predict(x_test)
            st.write("Accuracy: ",accuracy,round(2))
            st.write("Precision ", precision_score(y_test,y_pred,labels=class_names).round(2))
            st.write("Recall; ",recall_score(y_test,y_pred,labels=class_names).round(2))
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
            model.fit(x_train,y_train)
            accuracy=model.score(x_test,y_test)
            y_pred=model.predict(x_test)
            st.write("Accuracy: ",accuracy,round(2))
            st.write("Precision ", precision_score(y_test,y_pred,labels=class_names).round(2))
            st.write("Recall; ",recall_score(y_test,y_pred,labels=class_names).round(2))
            plot_metrics(metrics)    
    if st.sidebar.checkbox("Show raw data", False):
        st.subheader("Mushroom Data Set (Classification)")
        st.write(df)


if __name__ == '__main__':
    main()

