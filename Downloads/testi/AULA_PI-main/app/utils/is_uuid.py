from uuid import UUID

def is_uuid(text: str) -> bool:
  try:
    UUID(text)
    return True
  except ValueError:  
    return False
