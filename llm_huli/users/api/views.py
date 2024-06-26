import re

import numpy as np
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from llm_huli.users.models import User, File, word2vec_model, nlp

from .serializers import UserSerializer, TextUploadSerializer, TextFileUploadSerializer, TextFileSerializer


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

def preprocess_text(text):
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text
def get_embeddings(text: str):
    tokens = nlp(preprocess_text(text.lower()))
    word_vectors = [word2vec_model[token.text] for token in tokens if token.text in word2vec_model]
    if word_vectors:
        return np.mean(word_vectors, axis=0)  # Возвращаем среднее значение по оси 0 (одномерный массив)
    else:
        return None

class TextUploadView(APIView):

    def post(self, request):
        print(type(request.data))
        serializer = TextFileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            # Прочитать весь файл сразу
            uploaded_text = file.read().decode('utf-8')
            chunk_size = 200
            chunk_overlap = 50
            document_chunks = []

            for i in range(0, len(uploaded_text), chunk_size - chunk_overlap):
                chunk = uploaded_text[i:i + chunk_size]
                document_chunks.append(chunk)
            vectors = []
            texts = []
            for text in document_chunks:
                embedding = get_embeddings(text)
                if embedding is not None:
                    vectors.append(embedding)
                    texts.append(text)
            print(len(vectors))
            new_file = File.objects.create(file_vectors=vectors)
            return Response({'message': 'File uploaded successfully', 'content': new_file})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TextFileDetailView(RetrieveAPIView):
    queryset = File.objects.all()
    serializer_class = TextFileSerializer
