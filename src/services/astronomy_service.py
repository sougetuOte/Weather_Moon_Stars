"""
天体サービス実装

既存のmoon_age.pyとastrology.pyをラップし、データモデルに変換するサービス層
"""
import sys
import os

# パスを追加して既存モジュールをインポート可能に
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.data_models import AstronomyData
from services.interfaces import IAstronomyService, AstronomyServiceError


class AstronomyService(IAstronomyService):
    """天体サービス実装（既存機能のラッパー）"""
    
    def get_current_astronomy_data(self) -> AstronomyData:
        """
        現在の天体情報を取得
        
        既存のmoon_age.pyとastrology.pyの機能を統合して
        構造化されたAstronomyDataオブジェクトとして返す
        """
        try:
            # 既存のモジュールをインポート
            from features.moon_age import get_moon_age
            from features.astrology import get_moon_sign
            
            # 月齢を計算
            moon_age = get_moon_age()
            
            # 月齢から月相名を決定
            moon_phase_name = self._get_moon_phase_name(moon_age)
            
            # 月の星座情報を取得
            moon_zodiac, zodiac_description = get_moon_sign()
            
            # AstronomyDataオブジェクトを作成
            return AstronomyData(
                moon_age=moon_age,
                moon_phase_name=moon_phase_name,
                moon_zodiac=moon_zodiac,
                zodiac_description=zodiac_description
            )
            
        except ImportError as e:
            raise AstronomyServiceError(f"天体計算モジュールの読み込みに失敗: {str(e)}")
        except Exception as e:
            raise AstronomyServiceError(f"天体情報の取得中にエラーが発生: {str(e)}")
    
    def _get_moon_phase_name(self, moon_age: float) -> str:
        """
        月齢から月相名を決定
        
        Args:
            moon_age: 月齢（0-29.5）
            
        Returns:
            str: 月相名（新月、上弦、満月、下弦など）
        """
        if moon_age < 1.0:
            return "新月"
        elif moon_age < 6.5:
            return "三日月"
        elif moon_age < 8.5:
            return "上弦の月"
        elif moon_age < 13.5:
            return "十三夜月"
        elif moon_age < 15.5:
            return "満月"
        elif moon_age < 21.5:
            return "居待月"
        elif moon_age < 23.5:
            return "下弦の月"
        elif moon_age < 28.5:
            return "有明月"
        else:
            return "新月"