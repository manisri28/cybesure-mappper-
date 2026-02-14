def parse_sql(file):
    # 'file' here is the UploadFile object from FastAPI
    content = file.read()
    if isinstance(content, bytes):
        content = content.decode("utf-8")
    
    # Optional: Filter for security-relevant lines only
    security_keywords = ["password", "mfa", "login", "encrypted", "admin", "token", "access"]
    relevant_lines = []
    for line in content.split("\n"):
        if any(key in line.lower() for key in security_keywords):
            relevant_lines.append(line.strip())
            
    return " ".join(relevant_lines) if relevant_lines else content
