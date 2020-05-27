#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QSslConfiguration>
#include <QSslCertificate>
#include <QFile>
#include "reply.h"
#include "session.h"

Session::Session(const QUrl &server, QNetworkAccessManager *network, QObject *parent)
    : QObject(parent)
    , m_network(network)
    , m_server(server)
{
}

const QUrl &Session::getServer() const
{
    return m_server;
}

Reply *Session::get(const QUrl &uri, const QMap<QByteArray, QByteArray> &headers)
{
    return createReply(m_network->get(createRequest(uri, headers)));
}

Reply *Session::post(const QUrl &uri, const QByteArray &payload, const QMap<QByteArray, QByteArray> &headers)
{
    return createReply(m_network->post(createRequest(uri, headers), payload));
}

Reply *Session::put(const QUrl &uri, const QByteArray &payload, const QMap<QByteArray, QByteArray> &headers)
{
    return createReply(m_network->put(createRequest(uri, headers), payload));
}

Reply *Session::deleteResource(const QUrl &uri, const QMap<QByteArray, QByteArray> &headers)
{
    return createReply(m_network->deleteResource(createRequest(uri, headers)));
}

QUrl Session::completeUri(const QUrl &uri) const
{
    return QUrl(m_server.toString() + uri.toString());
}

QNetworkRequest Session::createRequest(const QUrl &uri, const QMap<QByteArray, QByteArray> &headers) const
{
    QNetworkRequest request(completeUri(uri));
    for (auto header : headers.toStdMap())
       request.setRawHeader(header.first, header.second);
    return request;
}

Reply *Session::createReply(QNetworkReply *networkReply)
{
    Reply *reply = new Reply(networkReply, this);
    connect(reply, &Reply::networkError, this, &Session::networkError);
    return reply;
}

void Session::setupCaCertificateFile(const QUrl &certificateFile)
{
    if (certificateFile.isEmpty())
        return;

    const QString filePath = certificateFile.scheme() == "qrc" ? certificateFile.toString().remove(0,3) // SessionTestCase
                                                               : certificateFile.toLocalFile();
    QFile fileResource(filePath);
    if (fileResource.open(QFile::ReadOnly)) {
        m_network->clearConnectionCache();
        QSslConfiguration sslConfiguration = QSslConfiguration::defaultConfiguration();
        sslConfiguration.setCaCertificates({QSslCertificate(&fileResource)});
        QSslConfiguration::setDefaultConfiguration(sslConfiguration);
    }
}
