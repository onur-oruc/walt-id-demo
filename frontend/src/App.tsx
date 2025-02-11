import { useEffect, useState } from 'react';
import { Box, Card, CardContent, Typography, Grid, Container, Switch, FormControlLabel, Divider } from '@mui/material';
import { getAllDids, getAllCredentials } from './services/api';

function App() {
  const [dids, setDids] = useState<any[]>([]);
  const [credentials, setCredentials] = useState<any[]>([]);
  const [selectedDid, setSelectedDid] = useState<string | null>(null);
  const [isBeautified, setIsBeautified] = useState(false);
  const walletId = import.meta.env.VITE_OEM_WALLET_ID;

  useEffect(() => {
    const fetchData = async () => {
      try {
        const didsData = await getAllDids();
        setDids(didsData);
        const credsData = await getAllCredentials();
        setCredentials(credsData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);

  const getLastComponent = (did: string) => {
    return did.split(':').pop();
  };

  const filteredCredentials = credentials.filter(
    cred => cred.parsedDocument?.credentialSubject?.id === selectedDid
  );

  const renderBeautifiedCredential = (cred: any) => {
    const sections = [
      {
        title: 'Basic Information',
        fields: [
          { label: 'Wallet', value: cred.wallet },
          { label: 'ID', value: cred.id },
          { label: 'Added On', value: new Date(cred.addedOn).toLocaleString() },
          { label: 'Owner', value: cred.parsedDocument?.credentialSubject?.id }
        ]
      },
      {
        title: 'Issuer',
        fields: [
          { label: 'Type', value: cred.parsedDocument?.issuer?.type?.join(', ') },
          { label: 'ID', value: cred.parsedDocument?.issuer?.id }
        ]
      },
      {
        title: 'Initial Data',
        fields: [
          { label: 'Type', value: cred.parsedDocument?.credentialSubject?.initialData?.type?.join(', ') },
          { label: 'Name', value: cred.parsedDocument?.credentialSubject?.initialData?.name },
          { label: 'Description', value: cred.parsedDocument?.credentialSubject?.initialData?.description }
        ]
      },
      {
        title: 'Quality Control',
        fields: [
          { label: 'Test Results', value: cred.parsedDocument?.credentialSubject?.initialData?.qualityControl?.testResults },
          { label: 'Inspector', value: cred.parsedDocument?.credentialSubject?.initialData?.qualityControl?.inspector },
          { label: 'Test Date', value: cred.parsedDocument?.credentialSubject?.initialData?.qualityControl?.testDate }
        ]
      },
      {
        title: 'Technical Details',
        fields: [
          { label: 'Capacity', value: cred.parsedDocument?.credentialSubject?.initialData?.technicalDetails?.capacity },
          { label: 'Chemistry', value: cred.parsedDocument?.credentialSubject?.initialData?.technicalDetails?.chemistry },
          { label: 'Voltage', value: cred.parsedDocument?.credentialSubject?.initialData?.technicalDetails?.voltage },
          { label: 'Max Charge Current', value: cred.parsedDocument?.credentialSubject?.initialData?.technicalDetails?.maxChargeCurrent },
          { label: 'Operating Temperature', value: cred.parsedDocument?.credentialSubject?.initialData?.technicalDetails?.operatingTemperature }
        ]
      }
    ];

    return (
      <Card>
        <CardContent>
          {sections.map((section, idx) => (
            <Box key={idx} sx={{ mb: 3 }}>
              <Typography variant="h6" color="primary" gutterBottom>
                {section.title}
              </Typography>
              <Grid container spacing={2}>
                {section.fields.map((field, fieldIdx) => (
                  <Grid item xs={12} sm={6} key={fieldIdx}>
                    <Typography variant="subtitle2" color="textSecondary">
                      {field.label}:
                    </Typography>
                    <Typography sx={{ wordBreak: 'break-all' }}>
                      {field.value || 'N/A'}
                    </Typography>
                  </Grid>
                ))}
              </Grid>
              {idx < sections.length - 1 && <Divider sx={{ mt: 2 }} />}
            </Box>
          ))}
        </CardContent>
      </Card>
    );
  };

  return (
    <Container>
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" gutterBottom>
          OEM Wallet ID: {walletId}
        </Typography>

        <Typography variant="h5" gutterBottom>
          DIDs
        </Typography>
        <Grid container spacing={2}>
          {dids.map((did) => (
            <Grid item xs={12} sm={6} md={4} key={did.did}>
              <Card 
                onClick={() => setSelectedDid(did.did)}
                sx={{ 
                  cursor: 'pointer', 
                  bgcolor: selectedDid === did.did ? '#e3f2fd' : 'white',
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column'
                }}
              >
                <CardContent>
                  <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                    DID:
                  </Typography>
                  <Typography 
                    sx={{ 
                      wordBreak: 'break-all',
                      mb: 2
                    }}
                  >
                    {did.did}
                  </Typography>
                  <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                    Internal ID:
                  </Typography>
                  <Typography sx={{ wordBreak: 'break-all' }}>
                    {getLastComponent(did.did)}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        {selectedDid && (
          <Box sx={{ mt: 4 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h5">
                Credentials for {selectedDid}
              </Typography>
              <FormControlLabel
                control={<Switch checked={isBeautified} onChange={(e) => setIsBeautified(e.target.checked)} />}
                label="Beautify"
              />
            </Box>
            <Grid container spacing={2}>
              {filteredCredentials.map((cred, index) => (
                <Grid item xs={12} key={index}>
                  {isBeautified ? (
                    renderBeautifiedCredential(cred)
                  ) : (
                    <Card>
                      <CardContent>
                        <pre>{JSON.stringify(cred, null, 2)}</pre>
                      </CardContent>
                    </Card>
                  )}
                </Grid>
              ))}
            </Grid>
          </Box>
        )}
      </Box>
    </Container>
  );
}

export default App;
