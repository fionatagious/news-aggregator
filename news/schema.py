import graphene
from graphene_django import DjangoObjectType
from news.models import Article, Comment

# Type definitions
# DjangoObjectType subclasses that represent the GraphQL types for the Article and Comment models.
class ArticleType(DjangoObjectType):
  class Meta:
    model = Article
    fields = ("title", "body", "pub_date")

class CommentType(DjangoObjectType):
  class Meta:
    model = Comment
    fields = ("article", "comment_text", "votes")

# Query definition - fetch data
class Query(graphene.ObjectType):
  all_articles = graphene.List(ArticleType)
  article_by_id = graphene.Field(ArticleType, id=graphene.Int())
  all_comments = graphene.List(CommentType)
  comments_by_article = graphene.List(CommentType, article_id=graphene.Int())

  # Resolve methods
  def resolve_all_articles(self, info):
    return Article.objects.all()

  def resolve_article_by_id(self, info, id):
    return Article.objects.get(id=id)

  def resolve_all_comments(self, info):
    return Comment.objects.all()

  def resolve_comments_by_article(self, info, article_id):
    return Comment.objects.filter(article_id=article_id)

# Mutation definition - create or update data
class CreateArticle(graphene.Mutation):
  class Arguments:
    title = graphene.String(required=True)
    body = graphene.String(required=True)

  article = graphene.Field(ArticleType)

  def mutate(self, info, title, body):
    article = Article.objects.create(title=title, body=body)
    return CreateArticle(article=article)

class CreateComment(graphene.Mutation):
  class Arguments:
    article_id = graphene.Int(required=True)
    comment_text = graphene.String(required=True)

  comment = graphene.Field(CommentType)

  def mutate(self, info, article_id, comment_text):
    article = Article.objects.get(id=article_id)
    comment_text = Comment.objects.create(article=article, comment_text=comment_text)
    return CreateComment(comment_text=comment_text)

class Mutation(graphene.ObjectType):
  create_article = CreateArticle.Field()
  create_comment = CreateComment.Field()

# Schema definition
schema = graphene.Schema(query=Query, mutation=Mutation)