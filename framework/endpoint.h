#pragma once

#include <QQmlEngine>
#include <QObject>

class Session;
class Reply;

class Endpoint : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QJSValue callback READ getCallback WRITE setCallback NOTIFY callbackChanged)

protected:
    Endpoint(const QJSValue &callback, Session *parent, QJSEngine *jsEng, QQmlEngine *qmlEng);

    void setHeader(const QByteArray &header, const QByteArray &value);
    void setBaseUri(const QUrl &uri);
    void setBaseUriQuery(const QUrlQuery &query);

    Reply *httpPost(const QByteArray &payload);
    Reply *httpGet();
    Reply *httpPut(const QByteArray &payload);
    Reply *httpDelete();

    void callback(const int statusCode, const QByteArray &data, const QMap<int, bool> &codes, const QJSValueList &arguments);

    QQmlEngine *getQmlEngine();

    template <typename T>
    QJSValue jsArg(const T &value) {
        return m_jsEngine->toScriptValue(value);
    }

signals:
    void callbackChanged();

public:
    const QJSValue &getCallback() const;
    void setCallback(const QJSValue &callback);

private:
    Reply *adoptReply(Reply *reply);

private:
    QMap<QByteArray, QByteArray> m_headers;
    QUrl                         m_baseUri;
    QJSValue                     m_callback;
    Session                      *m_session;
    QJSEngine                    *m_jsEngine;
    QQmlEngine                   *m_qmlEngine;
};
