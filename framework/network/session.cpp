#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QFile>
#include <QSslCertificate>
#include "reply.h"
#include "session.h"

Session::Session(const QUrl &server, QNetworkAccessManager *network, QObject *parent)
    : QObject(parent)
    , m_network(network)
    , m_server(server)
    , m_sslConfiguration(QSslConfiguration::defaultConfiguration())
{
}

const QUrl &Session::getServer() const
{
    return m_server;
}

Reply *Session::get(const QUrl &uri, const QMap<QByteArray, QByteArray> &headers)
{
    return new Reply(m_network->get(createRequest(uri, headers)), this);
}

Reply *Session::post(const QUrl &uri, const QByteArray &payload, const QMap<QByteArray, QByteArray> &headers)
{
    return new Reply(m_network->post(createRequest(uri, headers), payload), this);
}

Reply *Session::put(const QUrl &uri, const QByteArray &payload, const QMap<QByteArray, QByteArray> &headers)
{
    return new Reply(m_network->put(createRequest(uri, headers), payload), this);
}

Reply *Session::deleteResource(const QUrl &uri, const QMap<QByteArray, QByteArray> &headers)
{
    return new Reply(m_network->deleteResource(createRequest(uri, headers)), this);
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

    request.setSslConfiguration(m_sslConfiguration);

    return request;
}

void Session::setupCaCertificateFile(const QString &certificateFile)
{
    if (certificateFile.isEmpty())
        return;

    QFile fileResource(certificateFile);
    if (fileResource.open(QFile::ReadOnly))
        m_sslConfiguration.setCaCertificates({QSslCertificate(&fileResource)});
}
