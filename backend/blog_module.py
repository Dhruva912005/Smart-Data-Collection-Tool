import os
import random
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_blog_pdf(topic, num_pages=1):
    
    intros = [
        f"The concept of {topic} has fundamentally altered modern paradigms.",
        f"When observing the rapid expansion of {topic}, several undeniable patterns emerge.",
        f"In recent years, {topic} has transitioned from a niche interest to a global focal point.",
        f"Understanding the nuances of {topic} requires both historical perspective and forward-looking analysis.",
        f"As societal demands evolve, the relevance of {topic} continues to scale exponentially.",
        f"Few phenomena demonstrate the interconnected nature of today's systems quite like {topic}.",
        f"Addressing the challenges within {topic} is paramount for sustainable long-term development.",
        f"At the forefront of the current generation's innovation lies the undeniable impact of {topic}.",
        f"Examining {topic} provides profound insights into modern structural shifts.",
        f"The underlying mechanics of {topic} have garnered significant attention globally."
    ]

    body_transitions = [
        "Furthermore, ", "Moreover, ", "In particular, ", "For instance, ", 
        "Interestingly, ", "Consequently, ", "As a result, ", "On another note, ",
        "Specifically, ", "Importantly, ", "Notably, ", "By comparison, ",
        "In addition, ", "Simultaneously, ", "Looking deeper, "
    ]
    
    body_core = [
        "this development necessitates a shift in traditional operational models.",
        f"experts suggest that {topic} will redefine resource allocation across industries.",
        "technological integration plays a pivotal role in these advancing metrics.",
        "shifting consumer sentiment directly influences these underlying structural elements.",
        "market volatility often acts as a catalyst for unprecedented architectural growth.",
        "regulatory frameworks are slowly adapting to accommodate these novel mechanisms.",
        f"institutional investment regarding {topic} has seen a sharp, sustained acceleration.",
        "underlying data strongly supports a bullish long-term macro perspective.",
        "competitive forces are pushing stakeholders to adopt highly agile strategies.",
        "the barrier to entry is continuously lowering due to widespread digitization.",
        "historical comparisons reveal parallel growth trajectories in adjacent sectors.",
        "advanced analytical models predict significant paradigm shifts within the decade.",
        f"the societal integration of {topic} bridges critical communication gaps.",
        "strategic partnerships are forming rapidly to capitalize on this momentum."
    ]

    body_expansions = [
        "This clearly signals a departure from legacy systems.",
        "However, implementing these changes remains highly complex.",
        "Consequently, organizations prioritizing agility hold a distinct advantage.",
        "It inevitably raises questions regarding security, scalability, and ethical compliance.",
        "Thus, a multidisciplinary approach is highly recommended for optimal synthesis.",
        "Such insights reinforce the absolute necessity of continued, deep-rooted research.",
        "Bridging this gap will require collaborative efforts across multiple sectors.",
        "This dynamic environment heavily rewards early adopters and strategic visionaries.",
        "Failure to recognize these shifts may result in significant structural disadvantages.",
        "These developments illuminate a path toward unprecedented global efficiency."
    ]

    conclusions = [
        f"Ultimately, the trajectory of {topic} points toward sustained, transformative impact.",
        f"In conclusion, embracing the complexities of {topic} is essential for future readiness.",
        "To summarize, proactive adaptation is the only viable strategy in this changing landscape.",
        f"Looking ahead, {topic} will undoubtedly serve as a foundational pillar of modern infrastructure.",
        "Final analyses dictate that ignoring these trends carries substantial opportunity risks.",
        "The evidence is clear: the paradigm has shifted, and recalibration is mandatory.",
        f"As we navigate the coming years, {topic} will remain a critical touchstone for success.",
        "Synthesizing these elements provides a comprehensive roadmap for long-term viability.",
        f"The continued evolution of {topic} will likely dictate the next era of development.",
        "In synthesis, strategic foresight remains paramount when engaging with these variables."
    ]

    used_sentences = set()
    paragraphs = []
    stopped_early = False

    def get_unique_sentence(pool_list):
        random.shuffle(pool_list)
        for cand in pool_list:
            if cand not in used_sentences:
                used_sentences.add(cand)
                return cand
        
        modifier = random.choice(["Indeed, ", "It is evident that ", "Research confirms ", "Significantly, "])
        fallback = f"{modifier}{random.choice(pool_list).lower()}"
        
        count = 0
        while fallback in used_sentences and count < 100:
            modifier = random.choice(["Indeed, ", "It is evident that ", "Research confirms ", "Significantly, "])
            fallback = f"{modifier}{random.choice(pool_list).lower()}"
            count += 1
            
        if count >= 100:
            raise ValueError("Exhausted unique combinations")
            
        used_sentences.add(fallback)
        return fallback

    def build_body_sentence(attempts=0):
        if attempts >= 100:
            raise ValueError("Exhausted unique combinations")
            
        transition = random.choice(body_transitions)
        core = random.choice(body_core)
        expansion = random.choice(body_expansions)
        
        sentence = f"{transition}{core} {expansion}"
        
        if sentence in used_sentences:
            return build_body_sentence(attempts + 1)
            
        used_sentences.add(sentence)
        return sentence

    try:
        # Intro Phase
        intro_sentences = []
        for _ in range(5):
            intro_sentences.append(get_unique_sentence(intros))
        paragraphs.append(" ".join(intro_sentences))

        # Body Phase: (num_pages * 6) paragraphs minus 2
        total_body_paras = (num_pages * 6) - 2
        for _ in range(max(1, total_body_paras)):
            body_sents = []
            for _ in range(5):
                body_sents.append(build_body_sentence())
            paragraphs.append(" ".join(body_sents))
            
        # Conclusion Phase
        conclusion_sentences = []
        for _ in range(5):
            conclusion_sentences.append(get_unique_sentence(conclusions))
        paragraphs.append(" ".join(conclusion_sentences))

    except ValueError:
        # If mathematically exhausted, we safely trap the error to render structurally partial outputs
        stopped_early = True

    # create PDF
    os.makedirs("data", exist_ok=True)
    file_path = f"data/{topic.replace(' ', '_')}_blog.pdf"
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    content = []

    title_style = styles["Heading1"]
    content.append(Paragraph(topic.upper(), title_style))
    content.append(Spacer(1, 16))

    for para_text in paragraphs:
        content.append(Paragraph(para_text, styles["Normal"]))
        content.append(Spacer(1, 12))

    doc.build(content)
    print("PDF Generated!")
    
    return file_path, stopped_early