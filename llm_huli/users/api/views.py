from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from llm_huli.users.models import User, word2vec_model, nlp

from .serializers import UserSerializer, TextUploadSerializer


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


class TextUploadView(APIView):

    def post(self, request):
        serializer = TextUploadSerializer(data=request.data)

        if serializer.is_valid():
            # Process the text (for example, save to database)
            uploaded_text = serializer.validated_data['text']
            print(uploaded_text)
            # Here you can perform any actions with the uploaded text
            # For example, save it to a database
            tokens = nlp(preprocess_text(text.lower()))
            word_vectors = [word2vec_model[token.text] for token in tokens if token.text in word2vec_model]
            if word_vectors:
                print(sum(word_vectors) / len(word_vectors))
            # Assuming some hypothetical database model:
            # MyModel.objects.create(text=uploaded_text)

            return Response({"message": "Text uploaded successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
