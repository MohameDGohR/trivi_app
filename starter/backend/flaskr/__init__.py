import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
from typing import List




QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app,)

  
  
  @app.after_request
  def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*") 
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

        
   
    

  
  questions_in_page= 10
  def paginate_questions(request, selection):
        #take the page of from user or make it defaults as 1  
        page = request.args.get('page', 1, type=int)
        # determine the questions start from it in list   
        start =  (page - 1) * questions_in_page
        #determine the end of question  in list 
        end = start + questions_in_page
        # make question in specific formate defined in  class questions
        questions = [question.format() for question in selection]
        #take questions from list from start position to end position
        current_questions = questions[start:end]
        #return list of questions that will be shown for user
        return current_questions

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
          #get object  from database 
          question = Question.query.filter(Question.id == question_id).one_or_none()

          if question is None:
                abort(404)
          #delete object 
          question.delete()
          return jsonify({
                'success': True,
                'id':question_id
                 })
    except:
      abort(422)
  @app.route('/questions')
  def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_qustions = paginate_questions(request, selection)
        if len(current_qustions) == 0:
              abort(404)
        categories_formate = [Category.format() for Category in Category.query.all()]
        categories = {}

        for cat in categories_formate:
              categories[cat[0]]=cat[1]
        
        return jsonify({
          'success': True,
          'questions': current_qustions,
          'totalQuestions': len(Question.query.all()),
          'categories':categories,
          'currentCategory':'all'
   
           })

      

  questions_forplay= []
  current_category1 = None
  @app.route('/quizzes',methods=['POST'])
  def do_quize():
        body = request.get_json()
        question_prev = body.get('previous_questions', None)
        category =  body.get('quiz_category', None)
        
        query_check = Category.query.filter(Category.type == category['type'])
        query_check2 = Question.query.filter(Question.category == str(category['id']))
        
        if category is None or  query_check.count() < 1 or  query_check2.count() < 1:
              if  category['type'] != 'click' :
                    return jsonify({
                    'success': False })
                    
              
       
        #current_category1 = category['type']  
         
         
        if  len(question_prev) == 0 and  category is not None   and (query_check.count() > 0 )  :
              
              questions_forplay.clear()

              selection = Question.query.order_by(Question.id).filter(Question.category== str(category['id']) ).all()
              
             
              if len(selection) == 0 :
                    abort(404)
              for x in selection :
                    questions_forplay.append(x.id)
              
              random_num = random.choice(questions_forplay)
              questions_forplay.remove(random_num)
              question_result = Question.query.get(random_num)
              return jsonify({
                    'success': True,
                    'question':question_result.format() 
                    })
        elif  len(question_prev) > 0 and category is not None and len(questions_forplay) > 0  and query_check.count() > 0  :
              
               random_num = random.choice(questions_forplay)
               questions_forplay.remove(random_num)
               question_result = Question.query.get(random_num)
               return jsonify({
                    'success': True,
                    'question':question_result.format() 
                    })
        elif category['type'] == 'click' and  category['id'] ==  0 and len(question_prev) == 0:
              questions_forplay.clear()

              selection = Question.query.all()
              
             
              if len(selection) == 0 :
                    abort(404)
              for x in selection :
                    questions_forplay.append(x.id)
              
              random_num = random.choice(questions_forplay)
              questions_forplay.remove(random_num)
              question_result = Question.query.get(random_num)
              return jsonify({
                    'success': True,
                    'question':question_result.format() 
                    })
        elif len(question_prev) > 0 and category is not None and len(questions_forplay) > 0 and category['type'] == 'click':
              #take random element from list questions_forplay 
              random_num = random.choice(questions_forplay)
              # remove random_num element from questions_forplay
              questions_forplay.remove(random_num)
              #get question  from database  by id we took it from list  questions_forplay
              question_result = Question.query.get(random_num)
              return jsonify({
                    'success': True,
                    'question':question_result.format() 
                    })
        else:
              return jsonify({
                    'success': False })

               

       
       
        
        


   
              

        

  @app.route('/categories/<int:category_id>/questions')
  def get_category_questions(category_id):
        try:
              questions_result =  Question.query.filter_by(category = str(category_id)).all()
              if  questions_result is None  :
                    abort(404)
              questions = [question.format() for question in questions_result] 
              category_val = Category.query.get(category_id).format()
              if  category_val == None:
                    abort(404)
              category={}
              category[category_val[0]]=category_val[1]

              return jsonify({
                    "questions":questions,
                    "totalQuestions":len(questions),
                    "currentCategory":category
                      })      
        except:

              abort(422)  

  @app.route('/questions',methods=['POST'])
  def search_question():
        body = request.get_json()
        search = body.get('searchTerm', None)
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty',  None)
        new_category = body.get('category', None)
        try:
              if search :
                     
                     selection =Question.query.filter(Question.question.ilike('%' +search+ '%')).all()
                     if   len(selection) ==  0 :
                           abort(404)
                     current_questions = paginate_questions(request, selection)
                     categories_formate =  Category.query.get(selection[0].category).format()
                     categories = {}
                     categories[categories_formate[0]]=  categories_formate[1]
                    
                     return jsonify({
                            "success":True,
                            "questions": current_questions,
                            "totalQuestions": len(selection),
                            "currentCategory": categories 
                            })
              elif  new_question != None and new_answer != None and  new_difficulty!= None and new_category!= None :
                    question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty,
                    category=new_category)
                    question.insert()
                    return jsonify({
                          "success":True,
                          'created':question.id
                          })
              else:
                    abort(404)
        except:
              abort(422)
        
 


  
  @app.route('/categories')
  def get_categories():
        categories_value = Category.query.order_by(Category.id).all()
        
        
        if len(categories_value) == 0:
              abort(404)
             
        categories_formate = [Category.format() for Category in categories_value]
        categories = {}

        for cat in categories_formate:
              categories[cat[0]]=cat[1]
        
        
        return jsonify({
          'success': True,
          'categories': categories,
          })
        
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404
   
  
 
  return app

    