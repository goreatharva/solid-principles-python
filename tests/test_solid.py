
import types
import pytest

# SRP
from src.srp_report import Report, ReportSaver
# OCP
from src.ocp_discount import PriceCalculator, PercentageDiscount, FlatDiscount, DiscountStrategy
# LSP
from src.lsp_media import AudioPlayer, VideoPlayer, total_play_time, Player
# ISP
from src.isp_notifier import BasicEmailService, BasicSMSService, EmailNotifier, SMSNotifier
# DIP
from src.dip_order import Order, OrderProcessor, FakeGateway, PaymentGateway



def test_srp_report_render_and_save(tmp_path):
    rpt = Report(title='Daily', lines=['A', 'B'])
    content = rpt.render_text()
    assert 'Daily' in content and 'A' in content and 'B' in content

    saver = ReportSaver()
    file_path = tmp_path / 'report.txt'
    saver.save_to_file(content, file_path.as_posix())

    with open(file_path, 'r', encoding='utf-8') as f:
        saved = f.read()
    assert saved == content



def test_ocp_calculator_with_two_strategies():
    calc = PriceCalculator(PercentageDiscount(10))
    assert pytest.approx(calc.total(100.0), 0.001) == 90.0

    calc = PriceCalculator(FlatDiscount(15))
    assert pytest.approx(calc.total(100.0), 0.001) == 85.0


def test_ocp_extend_without_modifying_core():
    class ThresholdDiscount(DiscountStrategy):  
        def __init__(self, threshold: float, percent: float):
            self.threshold = threshold
            self.percent = percent
        def apply(self, price: float) -> float:
            if price >= self.threshold:
                return price * (1 - self.percent / 100)
            return price

    calc = PriceCalculator(ThresholdDiscount(200, 20))
    assert pytest.approx(calc.total(250), 0.001) == 200.0
    assert pytest.approx(calc.total(150), 0.001) == 150.0



def test_lsp_substitutability_and_total_time():
    players: list[Player] = [AudioPlayer(30), VideoPlayer(45, has_subtitles=True)]
    total = total_play_time(players)
    assert total == 75


def test_lsp_contract_non_negative():
    p = AudioPlayer(-10)
    assert p.play() >= 0



def test_isp_segregated_notifiers():
    mail = BasicEmailService()
    sms = BasicSMSService()

    em = EmailNotifier(mail)
    em.notify('a@b.com', 'Hello', 'Body')
    assert mail.sent == [('a@b.com', 'Hello', 'Body')]

    sm = SMSNotifier(sms)
    sm.notify('+910000000000', 'Hi')
    assert sms.sent == [('+910000000000', 'Hi')]



def test_dip_successful_checkout_generates_txn():
    order = Order([('x', 10.0), ('y', 15.0)])
    gateway = FakeGateway(will_succeed=True)
    proc = OrderProcessor(gateway)
    txn = proc.checkout(order, 'INR')
    assert txn.startswith('TXN-')
    assert gateway.charges == [(25.0, 'INR')]


def test_dip_failed_payment_raises():
    order = Order([('x', 10.0)])
    gateway = FakeGateway(will_succeed=False)
    proc = OrderProcessor(gateway)
    with pytest.raises(RuntimeError):
        proc.checkout(order)


def test_dip_invalid_order_total():
    order = Order([])
    gateway = FakeGateway()
    proc = OrderProcessor(gateway)
    with pytest.raises(ValueError):
        proc.checkout(order)
