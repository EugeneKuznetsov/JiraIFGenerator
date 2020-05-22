#include <QTest>
#include <QSignalSpy>
#include <QVariant>
#include "cutemockserver.h"
#include "session.h"
#include "reply.h"
#include "test_session.h"

void SessionTestCase::testGetOffline()
{
    QNetworkAccessManager network;
    Session session(QUrl("http://a.b.c.d.x.y.z:8080"), &network, nullptr);

    Reply *reply = session.get(QUrl(""), {});

    QVERIFY(reply != nullptr);
    QSignalSpy errorSpy(reply, &Reply::networkError);
    QVERIFY(errorSpy.wait(500));
}

void SessionTestCase::testGetOnline_data()
{
    QTest::addColumn<ushort>("port");
    QTest::addColumn<bool>("secure");
    QTest::addColumn<QString>("certificate");
    QTest::addColumn<QUrl>("server");
    QTest::addColumn<QString>("method");
    QTest::addColumn<int>("statusCode");

    QTest::newRow("invalid") << ushort(8080) << false << "" << QUrl("http://localhost:8080") << "POST" << 404;
    QTest::newRow("valid") << ushort(8080) << false << "" << QUrl("http://localhost:8080") << "GET" << 200;
    QTest::newRow("valid secure") << ushort(4443) << true << ":/cute/mock/ssl/cert/localhost.crt" << QUrl("https://localhost:4443") << "GET" << 200;
}

void SessionTestCase::testGetOnline()
{
    QFETCH(ushort, port);
    QFETCH(bool, secure);
    QFETCH(QString, certificate);
    QFETCH(QUrl, server);
    QFETCH(QString, method);
    QFETCH(int, statusCode);
    CuteMockServer mockServer;
    mockServer.setHttpRoute(method, QUrl("/"), statusCode, "text/html", "");
    mockServer.listen(port, secure);
    QNetworkAccessManager network;
    Session session(server, &network, nullptr);
    session.setupCaCertificateFile(certificate);

    Reply *reply = session.get(QUrl(""), {});

    QVERIFY(reply != nullptr);
    QSignalSpy readySpy(reply, &Reply::ready);
    QVERIFY(readySpy.wait(500));
    auto arguments = readySpy.takeFirst();
    QCOMPARE(arguments.at(0).toInt(), statusCode);
}

void SessionTestCase::testPostOffline()
{
    QNetworkAccessManager network;
    Session session(QUrl("http://a.b.c.d.x.y.z:8080"), &network, nullptr);

    Reply *reply = session.post(QUrl(""), "", {});

    QVERIFY(reply != nullptr);
    QSignalSpy errorSpy(reply, &Reply::networkError);
    QVERIFY(errorSpy.wait(500));
}

void SessionTestCase::testPostOnline_data()
{
    QTest::addColumn<ushort>("port");
    QTest::addColumn<bool>("secure");
    QTest::addColumn<QString>("certificate");
    QTest::addColumn<QUrl>("server");
    QTest::addColumn<QString>("method");
    QTest::addColumn<int>("statusCode");

    QTest::newRow("invalid") << ushort(8080) << false << "" << QUrl("http://localhost:8080") << "GET" << 404;
    QTest::newRow("valid") << ushort(8080) << false << "" << QUrl("http://localhost:8080") << "POST" << 200;
    QTest::newRow("valid secure") << ushort(4443) << true << ":/cute/mock/ssl/cert/localhost.crt" << QUrl("https://localhost:4443") << "POST" << 200;
}

void SessionTestCase::testPostOnline()
{
    QFETCH(ushort, port);
    QFETCH(bool, secure);
    QFETCH(QString, certificate);
    QFETCH(QUrl, server);
    QFETCH(QString, method);
    QFETCH(int, statusCode);
    CuteMockServer mockServer;
    mockServer.setHttpRoute(method, QUrl("/"), statusCode, "text/html", "");
    mockServer.listen(port, secure);
    QNetworkAccessManager network;
    Session session(server, &network, nullptr);
    session.setupCaCertificateFile(certificate);

    Reply *reply = session.post(QUrl(""), "", {});

    QVERIFY(reply != nullptr);
    QSignalSpy readySpy(reply, &Reply::ready);
    QVERIFY(readySpy.wait(500));
    auto arguments = readySpy.takeFirst();
    QCOMPARE(arguments.at(0).toInt(), statusCode);
}

void SessionTestCase::testPutOffline()
{
    QNetworkAccessManager network;
    Session session(QUrl("http://a.b.c.d.x.y.z:8080"), &network, nullptr);

    Reply *reply = session.put(QUrl(""), "", {});

    QVERIFY(reply != nullptr);
    QSignalSpy errorSpy(reply, &Reply::networkError);
    QVERIFY(errorSpy.wait(500));
}

void SessionTestCase::testPutOnline_data()
{
    QTest::addColumn<ushort>("port");
    QTest::addColumn<bool>("secure");
    QTest::addColumn<QString>("certificate");
    QTest::addColumn<QUrl>("server");
    QTest::addColumn<QString>("method");
    QTest::addColumn<int>("statusCode");

    QTest::newRow("invalid") << ushort(8080) << false << "" << QUrl("http://localhost:8080") << "GET" << 404;
    QTest::newRow("valid") << ushort(8080) << false << "" << QUrl("http://localhost:8080") << "PUT" << 200;
    QTest::newRow("valid secure") << ushort(4443) << true << ":/cute/mock/ssl/cert/localhost.crt" << QUrl("https://localhost:4443") << "PUT" << 200;
}

void SessionTestCase::testPutOnline()
{
    QFETCH(ushort, port);
    QFETCH(bool, secure);
    QFETCH(QString, certificate);
    QFETCH(QUrl, server);
    QFETCH(QString, method);
    QFETCH(int, statusCode);
    CuteMockServer mockServer;
    mockServer.setHttpRoute(method, QUrl("/"), statusCode, "text/html", "");
    mockServer.listen(port, secure);
    QNetworkAccessManager network;
    Session session(server, &network, nullptr);
    session.setupCaCertificateFile(certificate);

    Reply *reply = session.put(QUrl(""), "", {});

    QVERIFY(reply != nullptr);
    QSignalSpy readySpy(reply, &Reply::ready);
    QVERIFY(readySpy.wait(500));
    auto arguments = readySpy.takeFirst();
    QCOMPARE(arguments.at(0).toInt(), statusCode);
}

void SessionTestCase::testDeleteOffline()
{
    QNetworkAccessManager network;
    Session session(QUrl("http://a.b.c.d.x.y.z:8080"), &network, nullptr);

    Reply *reply = session.deleteResource(QUrl(""), {});

    QVERIFY(reply != nullptr);
    QSignalSpy errorSpy(reply, &Reply::networkError);
    QVERIFY(errorSpy.wait(500));
}

void SessionTestCase::testDeleteOnline_data()
{
    QTest::addColumn<ushort>("port");
    QTest::addColumn<bool>("secure");
    QTest::addColumn<QString>("certificate");
    QTest::addColumn<QUrl>("server");
    QTest::addColumn<QString>("method");
    QTest::addColumn<int>("statusCode");

    QTest::newRow("invalid") << ushort(8080) << false << "" << QUrl("http://localhost:8080") << "PUT" << 404;
    QTest::newRow("valid") << ushort(8080) << false << "" << QUrl("http://localhost:8080") << "DELETE" << 200;
    QTest::newRow("valid secure") << ushort(4443) << true << ":/cute/mock/ssl/cert/localhost.crt" << QUrl("https://localhost:4443") << "DELETE" << 200;
}

void SessionTestCase::testDeleteOnline()
{
    QFETCH(ushort, port);
    QFETCH(bool, secure);
    QFETCH(QString, certificate);
    QFETCH(QUrl, server);
    QFETCH(QString, method);
    QFETCH(int, statusCode);
    CuteMockServer mockServer;
    mockServer.setHttpRoute(method, QUrl("/"), statusCode, "text/html", "");
    mockServer.listen(port, secure);
    QNetworkAccessManager network;
    Session session(server, &network, nullptr);
    session.setupCaCertificateFile(certificate);

    Reply *reply = session.deleteResource(QUrl(""), {});

    QVERIFY(reply != nullptr);
    QSignalSpy readySpy(reply, &Reply::ready);
    QVERIFY(readySpy.wait(500));
    auto arguments = readySpy.takeFirst();
    QCOMPARE(arguments.at(0).toInt(), statusCode);
}

QTEST_GUILESS_MAIN(SessionTestCase)
