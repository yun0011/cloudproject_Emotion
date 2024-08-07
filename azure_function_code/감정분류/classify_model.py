import joblib
import os
import json
import logging
import azure.functions as func
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import re
import string

# 직렬화된 함수 재정의
@keras.saving.register_keras_serializable()
def clean_text(text):
    text = tf.strings.lower(text)
    text = tf.strings.regex_replace(text, f'[{re.escape(string.punctuation)}]', '')
    text = tf.strings.regex_replace(text, '\n', ' ')
    return text

MODEL_NAME = "classifymodel2.pkl"
TARGET_NAMES = ['positive', 'negative']

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("HTTP 트리거 함수가 요청을 처리했습니다.")

    try:
        model = load_model()
        req_body = req.get_json()
        data = req_body.get("data")

        if not data:
            raise ValueError("요청에 데이터가 제공되지 않았습니다.")

        logging.info(f"예측을 위한 데이터 수신: {data}")
        
        # 데이터를 리스트 형식으로 변환
        if isinstance(data, str):
            data = [data]

        # 데이터가 리스트의 리스트인 경우 플래트닝
        if isinstance(data[0], list):
            data = data[0]

        # 필요한 경우 Pandas Series로 변환
        data_series = pd.Series(data)

        y_pred = model.predict(data_series).argmax(axis=1)
        pred_classes = [TARGET_NAMES[y] for y in y_pred]

        logging.info(f"예측 결과: {pred_classes}")

        # Positive와 Negative의 비율 계산
        positive_count = pred_classes.count('positive')
        negative_count = pred_classes.count('negative')
        total_count = len(pred_classes)
        
        positive_percentage = (positive_count / total_count) * 100
        negative_percentage = (negative_count / total_count) * 100

        # ment 메시지 생성
        ment = f"당신의 행복지수는 지금 {positive_percentage:.2f}% 입니다:)"
        result = "positive" if positive_percentage >= 50 else "negative"

        response = {
            "classes": pred_classes,
            "result": result,
            "ment": ment
        }
        
        return func.HttpResponse(json.dumps(response), status_code=200)
    except Exception as e:
        logging.error(f"요청 처리 중 오류 발생: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500
        )

def load_model():
    path = os.path.join(os.path.dirname(__file__), MODEL_NAME)
    logging.info(f"{path}에서 모델을 로드 중입니다.")
    model = joblib.load(path)
    logging.info("모델이 성공적으로 로드되었습니다.")
    return model
