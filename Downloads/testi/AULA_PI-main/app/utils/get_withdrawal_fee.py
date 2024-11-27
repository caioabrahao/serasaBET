from decimal import Decimal

# This function is not used because all transactions are simulated but it 
# describes the logic of the platform's withdrawal fees.

def get_withdrawal_fee(value: Decimal) -> Decimal:
  if value <= 100:
    return value * Decimal('0.04')
  
  if value <= 1000:
    return value * Decimal('0.03')
  
  if value <= 5000:
    return value * Decimal('0.02')
  
  if value < 100_001:
    return value * Decimal('0.01')
  
  return Decimal('0')
