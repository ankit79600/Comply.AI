def process_chat(message: str) -> dict:
    msg = message.lower()
    
    # Simple language detection hack
    is_hindi = any(word in msg for word in ["kya", "kyu", "kyun", "mera", "kaise", "loan", "nahi", "tha", "mein"])
    
    if "denied" in msg or "why" in msg or "kyu" in msg or "kyun" in msg or "reason" in msg:
        if is_hindi:
            response = ("Aapka loan deny ho gaya tha kyunki aapka credit score 620 hai, jo ki hamare 680 ke requirement se kam hai. "
                        "Aur jankari ke liye, SHAP Analysis se pata chalta hai ki aapke zip code (location) ka bhi negative impact tha.")
            detected = "Hindi"
        else:
            response = ("Your loan was denied primarily because your credit score (620) is below our required threshold of 680. "
                        "SHAP analysis also indicates that your Zip Code negatively contributed to the algorithmic outcome.")
            detected = "English"
            
    elif "score" in msg or "credit" in msg:
        if is_hindi:
            response = "Aapka vartaman credit score 620 hai."
            detected = "Hindi"
        else:
            response = "Your current credit score is 620."
            detected = "English"
            
    elif "improve" in msg or "kaise" in msg or "better" in msg or "thik" in msg:
        if is_hindi:
            response = "Aap apne credit limit ka kam upyog karke aur bills time pe dekar apna score badha sakte hain."
            detected = "Hindi"
        else:
            response = "You can improve your score by maintaining a credit utilization rate below 30% and paying all bills on time."
            detected = "English"
            
    else:
        if is_hindi:
            response = "Maaf kijiye, main is mudde par madad nahi kar sakta. Kripya loan denial ya credit score ke baare mein puchein."
            detected = "Hindi"
        else:
            response = ("I'm sorry, I couldn't understand your request completely. Try asking 'Why was my loan denied?', "
                        "'What is my credit score?', or 'How can I improve it?'")
            detected = "English"
            
    return {
        "response": response,
        "detected_language": detected
    }
