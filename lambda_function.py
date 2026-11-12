# -*- coding: utf-8 -*-

import logging
import random
import time
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

QUIZ_QUESTIONS = [
    "What is the main purpose of a constructor in C++?",
    "What is the difference between a stack and a queue?",
    "What is a pointer, and how does it differ from a regular variable?",
    "What is the difference between pass-by-value and pass-by-reference?",
    "What does LIFO stand for in data structures?"
]

MAX_QUESTIONS = 3
MAX_TIME_SECONDS = 600


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = "Welcome to Study Buddy! You can say, quiz me on C plus plus, or teach me about pointers. What would you like to do?"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class QuizIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("QuizIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        topic_slot = slots.get("topic")
        
        topic_name = "general science"
        if topic_slot and topic_slot.value:
            topic_name = topic_slot.value

        # Prepare a shuffled list of questions for this session
        session_questions = list(QUIZ_QUESTIONS)
        random.shuffle(session_questions)
        current_question = session_questions.pop(0)

        session_attr = handler_input.attributes_manager.session_attributes
        session_attr['question_count'] = 1
        session_attr['score'] = 0
        session_attr['quiz_start_time'] = time.time()
        session_attr['remaining_questions'] = session_questions

        speak_output = f"Alright! Let's start a quiz on {topic_name}. Question 1 of {MAX_QUESTIONS}: {current_question}"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("What is your answer?")
                .response
        )


class TeachIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("TeachIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        topic_slot = slots.get("topic")
        
        topic_name = "general programming"
        if topic_slot and topic_slot.value:
            topic_name = topic_slot.value

        speak_output = f"I'd love to help you learn about {topic_name}. In short, it is a core concept that helps developers build structured, efficient logic. Would you like a quiz on this topic now?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Would you like a quiz on this?")
                .response
        )


class HelloWorldIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Hello World!"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class AnswerIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AnswerIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        answer_slot = slots.get("answer")
        
        user_answer = "your answer"
        if answer_slot and answer_slot.value:
            user_answer = answer_slot.value

        session_attr = handler_input.attributes_manager.session_attributes
        question_count = session_attr.get('question_count', 1)
        score = session_attr.get('score', 0) + 1
        start_time = session_attr.get('quiz_start_time', time.time())
        remaining_questions = session_attr.get('remaining_questions', [])

        elapsed_time = time.time() - start_time
        if elapsed_time > MAX_TIME_SECONDS:
            speak_output = "Time is up! You ran out of the 10-minute limit for this quiz session. Great effort though!"
            return handler_input.response_builder.speak(speak_output).response

        if question_count >= MAX_QUESTIONS:
            total_minutes = int(elapsed_time // 60)
            total_secs = int(elapsed_time % 60)
            speak_output = f"You answered: {user_answer}. That is correct! You have completed all {MAX_QUESTIONS} questions. Your final score is {score} out of {MAX_QUESTIONS}, completed in {total_minutes} minutes and {total_secs} seconds. Great job!"
            return handler_input.response_builder.speak(speak_output).response

        # Pull the next unique question from our remaining list
        next_question = remaining_questions.pop(0) if remaining_questions else "What is C++?"

        session_attr['question_count'] = question_count + 1
        session_attr['score'] = score
        session_attr['remaining_questions'] = remaining_questions
        
        speak_output = f"You answered: {user_answer}. That is correct! Here is question {question_count + 1} of {MAX_QUESTIONS}: {next_question}"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("What is your answer?")
                .response
        )


class YesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        session_questions = list(QUIZ_QUESTIONS)
        random.shuffle(session_questions)
        next_question = session_questions.pop(0)

        session_attr = handler_input.attributes_manager.session_attributes
        session_attr['question_count'] = 1
        session_attr['score'] = 0
        session_attr['quiz_start_time'] = time.time()
        session_attr['remaining_questions'] = session_questions

        speak_output = f"Awesome! Let's start your 3-question quiz session. Question 1 of {MAX_QUESTIONS}: {next_question}"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("What is your answer?")
                .response
        )


class NoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "No problem! Let me know if you want to explore another topic or take a quiz later."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "You can ask me to quiz you or teach you about a topic! How can I help?"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speak_output = "Goodbye!"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        speech = "Hmm, I'm not sure. You can ask me to quiz you on a topic. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"
        return handler_input.response_builder.speak(speech).ask(reprompt).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        speak_output = "Sorry, I had trouble doing what you asked. Please try again."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(QuizIntentHandler())
sb.add_request_handler(TeachIntentHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(AnswerIntentHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
