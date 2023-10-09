import sys
import os
import pandas as pd
import numpy as np
from dataclasses import dataclass #定义数据类

from sklearn.compose import ColumnTransformer #列转换器
from sklearn.impute import SimpleImputer #处理缺失值
from sklearn.pipeline import Pipeline #数据处理管道
from sklearn.preprocessing import OneHotEncoder,StandardScaler# 类型特征onehot编码，数值特征标准化处理（均值为0，方差为1）

from src.exception import CustomException #自定义异常处理
from src.logger import logging #自定义日志记录

from src.utils import save_object #将对象保存到文件中

@dataclass
class DataTransformationConfig:
  preprocessor_obj_file_path:str=os.path.join("artifacts","preprocessor.pkl")
  
class DataTransformation:
  def __init__(self):
    self.data_transformation_config=DataTransformationConfig()
  
  def get_data_transformer_obj(self):
    '''
    This function is responsible for data transformation.
    用管道对相应的特征列进行处理(填补缺失值，归一化处理，独热编码)
    '''
    try:
      numerical_columns=['reading score', 'writing score']
      categorical_columns=[
        'gender',
        'race/ethnicity',
        'parental level of education',
        'lunch',
        'test preparation course']
      
      num_pipeline=Pipeline(
        steps=[
          ("imputer",SimpleImputer(strategy="median")), #中位数填充
          ("scaler",StandardScaler())
        ]
      )
      
      cat_pipeline=Pipeline(
        steps=[
          ("imputer",SimpleImputer(strategy="most_frequent")), #众数
          ("one_hot_encoder",OneHotEncoder()),
          ("scaler",StandardScaler(with_mean=False))
        ]
      )
      
      logging.info(f"Categorical columns:{categorical_columns}")
      logging.info(f"Numerical columns:{numerical_columns}")
      
      preprocessor=ColumnTransformer(
        [
          ("num_pipelines",num_pipeline,numerical_columns),
          ("cat_pipelines",cat_pipeline,categorical_columns)
        ]
      )
      
      return preprocessor
    
    except Exception as e:
      raise CustomException
      
  def initiate_data_transformation(self,train_path,test_path):
    try:
      
      train_df=pd.read_csv(train_path) #根据文件路径读入训练集
      test_df=pd.read_csv(test_path)   #根据文件路径读入测试集 
      
      logging.info("Read train and test data completed")
      
      logging.info("Obtaining preprocessor object")
      
      preprocessoring_obj=self.get_data_transformer_obj() #建立数据预处理对象
      
      target_column_name="math score"
      numerical_columns=['reading score', 'writing score']
      
      input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1) #特征列
      target_feature_train_df=train_df[target_column_name] #标签列
      
      input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
      target_feature_test_df=test_df[target_column_name]
      
      logging.info("Applying preprocessoring object on training dataframe and test dataframe")
      
      #用数据预处理对象对特征列进行相应的管道处理：分类型特征补缺失值、独热编码；数值型特征补缺失值、归一化
      input_feature_train_arr=preprocessoring_obj.fit_transform(input_feature_train_df)
      input_feature_test_arr=preprocessoring_obj.transform(input_feature_test_df)
      
      #预处理完的数据类型是np.array,将标签列转换成np.array后，与特征列合并。
      train_arr=np.c_[
        input_feature_train_arr,np.array(target_feature_train_df)
      ]
      test_arr=np.c_[
        input_feature_test_arr,np.array(target_feature_test_df)
      ]

      logging.info("Saving preprocessoring object")#将预处理过程中用到的对象进行保存
      save_object(
        file_path=self.data_transformation_config.preprocessor_obj_file_path,
        obj=preprocessoring_obj
      )

      #返回数据处理完毕后的np.array数组（训练集、测试集），返回保存有数据预处理对象的文件路径
      return (
        train_arr,
        test_arr,
        self.data_transformation_config.preprocessor_obj_file_path,
      )
    except Exception as e:
      raise CustomException(e,sys)