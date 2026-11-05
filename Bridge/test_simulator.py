import ast, sys, json, re, os

def audit_file(file_path):
    if not os.path.exists(file_path):
        return {"status": "FAILED", "error": f"File not found: {file_path}"}
    
    ext = os.path.splitext(file_path)[1].lower()
    
    # 1. Python AST Validation
    if ext == ".py":
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                ast.parse(f.read())
            return {"status": "PASSED", "language": "Python", "message": "AST validation clean."}
        except SyntaxError as e:
            return {"status": "FAILED", "language": "Python", "error": str(e), "line": e.lineno}

    # 2. Unreal Engine C++20 Header/Source Macro Audit
    elif ext in [".h", ".hpp", ".cpp"]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        errors = []
        if ext in [".h", ".hpp"] and "UCLASS(" in content:
            if "GENERATED_BODY()" not in content:
                errors.append("UCLASS macro detected without mandatory GENERATED_BODY().")
            if not re.search(r'#include\s+["<].*generated\.h[">]', content):
                errors.append("Missing mandatory #include '*.generated.h' header anchor.")
        
        # Raw pointer warning for UObject types
        if re.search(r'\bU[A-Z]\w+\*\s+\w+;', content):
            errors.append("Raw UObject pointer detected. Enforce TObjectPtr<T> for UE 5.5 memory safety.")
            
        if errors:
            return {"status": "FAILED", "language": "C++20", "errors": errors}
        return {"status": "PASSED", "language": "C++20", "message": "Header macros & pointer safety verified."}

    return {"status": "SKIPPED", "message": f"Unsupported extension: {ext}"}

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else ""
    print(json.dumps(audit_file(target) if target else {"status": "NO_TARGET"}))
